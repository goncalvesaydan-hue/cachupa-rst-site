"""Validate the public model against contract v1 (docs/api-contract.md).

Every issue carries the field path and the reason. Requirements that only apply to
publication (contacts, address, hours, alt text, image files...) are errors in
production and warnings in preview, as the contract asks for honest previews
without fabricated values.
"""
import math
import re
from dataclasses import dataclass, field
from pathlib import Path
from urllib.parse import parse_qs, unquote, urlsplit

MODES = ('preview', 'production')
TOP_LEVEL = ('schemaVersion', 'preview', 'site', 'restaurant', 'pages',
             'artist', 'artworks', 'images', 'navigation')
PAGE_KEYS = ('home', 'house', 'gallery', 'reservations', 'contacts', 'privacy', 'notFound')
SECTION_TYPES = ('editorial', 'photoGrid', 'artworkSelection', 'visit')
CONTACT_FIELDS = ('phoneDisplay', 'phoneHref', 'whatsappDisplay', 'whatsappHref',
                  'emailDisplay', 'emailHref', 'directionsHref', 'socialLinks')
ARTIST_FIELDS = ('id', 'name', 'bio', 'portrait', 'website')
ARTWORK_FIELDS = ('id', 'artistId', 'title', 'year', 'technique', 'dimensions',
                  'description', 'imageId', 'fullImageId', 'order', 'featured')
IMAGE_FIELDS = ('id', 'src', 'width', 'height', 'alt', 'caption', 'credit',
                'variants', 'mobileImageId', 'focalPoint')
MIME_TYPES = ('image/avif', 'image/webp', 'image/jpeg', 'image/png')

_TIME = re.compile(r'([01]\d|2[0-3]):[0-5]\d')
_TEL = re.compile(r'tel:\+?\d{6,15}')
_WA_PATH = re.compile(r'/\d{8,15}')
_EMAIL = re.compile(r'[^\s@<>"\'?&]+@[^\s@<>"\'?&]+\.[^\s@<>"\'?&]+')


@dataclass(frozen=True)
class Issue:
    path: str
    message: str

    def __str__(self):
        return f'{self.path}: {self.message}'


@dataclass
class Report:
    errors: list = field(default_factory=list)
    warnings: list = field(default_factory=list)

    @property
    def ok(self):
        return not self.errors


def validate_model(model, mode='preview', public_dir=None):
    """Validate a normalized model. `public_dir`, when given, is the folder that
    serves `/` (frontend/public); referenced image files must exist there."""
    if mode not in MODES:
        raise ValueError(f'modo desconhecido: {mode!r}')
    checker = _Checker(mode == 'production', public_dir)
    checker.model(model)
    return Report(checker.errors, checker.warnings)


# --- value predicates ------------------------------------------------------------

def _text(value):
    return isinstance(value, str) and bool(value.strip())


def _is_int(value):
    return type(value) is int


def _is_number(value):
    return type(value) in (int, float) and math.isfinite(value)


def _safe_chars(value):
    return isinstance(value, str) and not any(ord(c) < 33 or c in '\\"<>' for c in value)


def _https_url(value):
    if not _safe_chars(value):
        return False
    try:
        parts = urlsplit(value)
        return parts.scheme == 'https' and bool(parts.hostname) and not parts.username and not parts.password
    except ValueError:
        return False


def _internal_path(value):
    if not _safe_chars(value) or not value.startswith('/') or value.startswith('//'):
        return False
    path = unquote(value.split('?')[0].split('#')[0])
    return '..' not in path.split('/') and not path.startswith('//')


def _asset_path(value):
    if not _safe_chars(value) or not value.startswith('/assets/'):
        return False
    return '..' not in unquote(value).split('/') and '//' not in value and '?' not in value


# --- checker -----------------------------------------------------------------------

class _Checker:
    def __init__(self, production, public_dir):
        self.production = production
        self.public_dir = Path(public_dir).resolve() if public_dir else None
        self.errors, self.warnings = [], []
        self.image_ids, self.artwork_ids = set(), set()

    def error(self, path, message):
        self.errors.append(Issue(path, message))

    def warn(self, path, message):
        self.warnings.append(Issue(path, message))

    def required_for_production(self, path, message):
        (self.error if self.production else self.warn)(path, message)

    def obj(self, path, value):
        if isinstance(value, dict):
            return True
        self.error(path, 'deve ser um objeto')
        return False

    def lst(self, path, value):
        if isinstance(value, list):
            return True
        self.error(path, 'deve ser uma lista')
        return False

    def no_unknown(self, path, value, allowed):
        for key in value:
            if key not in allowed:
                self.error(f'{path}.{key}', 'campo desconhecido no modelo público')

    def optional_text(self, path, value):
        if value is not None and not _text(value):
            self.error(path, 'deve ser texto não vazio ou null')

    def image_ref(self, path, value):
        if not isinstance(value, str):
            self.error(path, 'deve ser o ID de uma imagem')
        elif value not in self.image_ids:
            self.error(path, f'referência a imagem inexistente: {value!r}')

    # --- top level ---------------------------------------------------------------

    def model(self, model):
        if not self.obj('$', model):
            return
        self.no_unknown('$', model, TOP_LEVEL)
        for key in TOP_LEVEL:
            if key not in model:
                self.error(key, 'campo obrigatório em falta')

        if not _is_int(model.get('schemaVersion')) or model.get('schemaVersion') != 1:
            self.error('schemaVersion', 'deve ser o inteiro 1')
        preview = model.get('preview')
        if type(preview) is not bool:
            self.error('preview', 'deve ser booleano')
        elif preview == self.production:
            self.error('preview', 'deve ser false em produção' if self.production
                       else 'deve ser true em pré-visualização')

        images, artworks = model.get('images'), model.get('artworks')
        if isinstance(images, dict):
            self.image_ids = set(images)
        if isinstance(artworks, list):
            self.artwork_ids = {w.get('id') for w in artworks
                                if isinstance(w, dict) and isinstance(w.get('id'), str)}

        if 'site' in model:
            self.site(model['site'])
        if 'restaurant' in model:
            self.restaurant(model['restaurant'])
        if 'images' in model:
            self.images(images)
        if 'artist' in model:
            self.artist(model['artist'])
        if 'artworks' in model:
            self.artworks(artworks, model.get('artist'))
        if 'pages' in model:
            self.pages(model['pages'])
        if 'navigation' in model:
            self.navigation(model['navigation'])

    def site(self, site):
        if not self.obj('site', site):
            return
        self.no_unknown('site', site, ('name', 'locale', 'baseUrl'))
        if not _text(site.get('name')):
            self.error('site.name', 'nome do site obrigatório')
        if site.get('locale') != 'pt-PT':
            self.error('site.locale', 'deve ser "pt-PT"')
        base = site.get('baseUrl')
        if base is None:
            if self.production:
                self.warn('site.baseUrl', 'sem domínio definido: páginas publicadas sem URL canónico')
        elif not _https_url(base):
            self.error('site.baseUrl', 'deve ser null ou um URL https:// válido')

    # --- restaurant --------------------------------------------------------------

    def restaurant(self, restaurant):
        if not self.obj('restaurant', restaurant):
            return
        self.no_unknown('restaurant', restaurant, ('city', 'address', 'hours', 'contacts'))
        for key, label in (('city', 'cidade obrigatória'), ('address', 'morada obrigatória')):
            value = restaurant.get(key)
            if value is None:
                self.required_for_production(f'restaurant.{key}', f'{label} para produção')
            else:
                self.optional_text(f'restaurant.{key}', value)

        hours = restaurant.get('hours')
        if self.lst('restaurant.hours', hours):
            if not hours:
                self.required_for_production('restaurant.hours', 'horários obrigatórios para produção')
            self.hours(hours)

        if self.obj('restaurant.contacts', restaurant.get('contacts')):
            self.contacts(restaurant['contacts'])

    def hours(self, hours):
        seen = set()
        for i, day in enumerate(hours):
            path = f'restaurant.hours[{i}]'
            if not self.obj(path, day):
                continue
            self.no_unknown(path, day, ('day', 'closed', 'intervals', 'note'))
            number = day.get('day')
            if not _is_int(number) or not 1 <= number <= 7:
                self.error(f'{path}.day', 'deve ser um inteiro de 1 (segunda-feira) a 7 (domingo)')
            elif number in seen:
                self.error(f'{path}.day', 'dia repetido')
            else:
                seen.add(number)
            closed = day.get('closed')
            if type(closed) is not bool:
                self.error(f'{path}.closed', 'deve ser booleano')
            self.optional_text(f'{path}.note', day.get('note'))
            intervals = day.get('intervals')
            if not self.lst(f'{path}.intervals', intervals):
                continue
            if closed is True and intervals:
                self.error(f'{path}.intervals', 'um dia encerrado não tem intervalos')
            if closed is False and not intervals:
                self.error(f'{path}.intervals', 'um dia aberto precisa de pelo menos um intervalo')
            for j, interval in enumerate(intervals):
                self.interval(f'{path}.intervals[{j}]', interval)

    def interval(self, path, interval):
        if not self.obj(path, interval):
            return
        valid = True
        for key in ('opens', 'closes'):
            value = interval.get(key)
            if not isinstance(value, str) or not _TIME.fullmatch(value):
                self.error(f'{path}.{key}', 'deve usar o formato HH:MM (00:00–23:59)')
                valid = False
        next_day = interval.get('closesNextDay')
        if type(next_day) is not bool:
            self.error(f'{path}.closesNextDay', 'deve ser booleano')
            valid = False
        if valid and not next_day and interval['closes'] <= interval['opens']:
            self.error(f'{path}.closes', 'deve ser posterior a opens; usar closesNextDay=true '
                                          'para horários depois da meia-noite')

    def contacts(self, contacts):
        base = 'restaurant.contacts'
        self.no_unknown(base, contacts, CONTACT_FIELDS)
        for key in CONTACT_FIELDS:
            if key not in contacts:
                self.error(f'{base}.{key}', 'campo obrigatório em falta (usar null se desconhecido)')
        for key in ('phoneDisplay', 'whatsappDisplay', 'emailDisplay'):
            self.optional_text(f'{base}.{key}', contacts.get(key))

        checks = (
            ('phoneDisplay', 'phoneHref', self._tel, 'deve ser tel: seguido de 6 a 15 dígitos'),
            ('whatsappDisplay', 'whatsappHref', self._whatsapp,
             'deve ser https://wa.me/<número internacional> com mensagem codificada em ?text='),
            ('emailDisplay', 'emailHref', self._mailto,
             'deve ser mailto:<email válido> com assunto codificado'),
        )
        for display_key, href_key, check, message in checks:
            display, href = contacts.get(display_key), contacts.get(href_key)
            if href is not None and not check(href):
                self.error(f'{base}.{href_key}', message)
            if (display is None) != (href is None):
                self.error(f'{base}.{href_key}', f'{display_key} e {href_key} devem estar ambos '
                                                  'preenchidos ou ambos null')

        email, mailto = contacts.get('emailDisplay'), contacts.get('emailHref')
        if isinstance(email, str) and isinstance(mailto, str) and self._mailto(mailto):
            if unquote(urlsplit(mailto).path) != email:
                self.error(f'{base}.emailDisplay', 'deve ser o mesmo endereço usado em emailHref')

        if contacts.get('whatsappHref') is None:
            self.required_for_production(f'{base}.whatsappHref', 'WhatsApp obrigatório para produção')
        if contacts.get('emailHref') is None:
            self.required_for_production(f'{base}.emailHref', 'email obrigatório para produção')

        directions = contacts.get('directionsHref')
        if directions is not None and not _https_url(directions):
            self.error(f'{base}.directionsHref', 'deve ser null ou um URL https:// válido')

        links = contacts.get('socialLinks')
        if 'socialLinks' in contacts and self.lst(f'{base}.socialLinks', links):
            for i, link in enumerate(links):
                path = f'{base}.socialLinks[{i}]'
                if not self.obj(path, link):
                    continue
                if not _text(link.get('label')):
                    self.error(f'{path}.label', 'texto obrigatório')
                if not _https_url(link.get('href')):
                    self.error(f'{path}.href', 'deve ser um URL https:// válido')

    @staticmethod
    def _tel(value):
        return isinstance(value, str) and bool(_TEL.fullmatch(value))

    @staticmethod
    def _whatsapp(value):
        if not _safe_chars(value):
            return False
        try:
            parts = urlsplit(value)
        except ValueError:
            return False
        if parts.scheme != 'https' or parts.netloc != 'wa.me' or not _WA_PATH.fullmatch(parts.path):
            return False
        if parts.fragment:
            return False
        if not parts.query:
            return True
        query = parse_qs(parts.query, keep_blank_values=True)
        return set(query) == {'text'} and len(query['text']) == 1 and bool(query['text'][0].strip())

    @staticmethod
    def _mailto(value):
        if not _safe_chars(value):
            return False
        try:
            parts = urlsplit(value)
        except ValueError:
            return False
        if parts.scheme != 'mailto' or not _EMAIL.fullmatch(unquote(parts.path)) or parts.fragment:
            return False
        if not parts.query:
            return True
        query = parse_qs(parts.query, keep_blank_values=True)
        return set(query) <= {'subject', 'body'} and all(len(v) == 1 for v in query.values())

    # --- pages ---------------------------------------------------------------------

    def pages(self, pages):
        if not self.obj('pages', pages):
            return
        for key in pages:
            if key not in PAGE_KEYS:
                self.error(f'pages.{key}', 'página desconhecida no contrato v1')
        for key in PAGE_KEYS:
            path = f'pages.{key}'
            if key not in pages:
                self.error(path, 'página obrigatória em falta')
                continue
            page = pages[key]
            if not self.obj(path, page):
                continue
            self.no_unknown(path, page, ('title', 'description', 'heading', 'intro',
                                         'heroImageId', 'sections'))
            if not _text(page.get('title')):
                self.error(f'{path}.title', 'título obrigatório')
            for name in ('description', 'heading', 'intro'):
                self.optional_text(f'{path}.{name}', page.get(name))
            if page.get('description') is None:
                self.required_for_production(f'{path}.description', 'descrição obrigatória para produção')
            if page.get('heading') is None:
                self.required_for_production(f'{path}.heading', 'título visível obrigatório para produção')
            if page.get('heroImageId') is not None:
                self.image_ref(f'{path}.heroImageId', page['heroImageId'])
            if self.lst(f'{path}.sections', page.get('sections')):
                self.sections(f'{path}.sections', page['sections'])

    def sections(self, base, sections):
        ids = set()
        for i, section in enumerate(sections):
            path = f'{base}[{i}]'
            if not self.obj(path, section):
                continue
            self.no_unknown(path, section, ('id', 'type', 'heading', 'paragraphs',
                                            'imageIds', 'artworkIds', 'links'))
            section_id = section.get('id')
            if not _text(section_id):
                self.error(f'{path}.id', 'identificador estável obrigatório')
            elif section_id in ids:
                self.error(f'{path}.id', f'identificador repetido na página: {section_id!r}')
            else:
                ids.add(section_id)
            if not isinstance(section.get('type'), str) or section['type'] not in SECTION_TYPES:
                self.error(f'{path}.type', 'tipo inválido; usar ' + ', '.join(SECTION_TYPES))
            self.optional_text(f'{path}.heading', section.get('heading'))

            paragraphs = section.get('paragraphs', [])
            if self.lst(f'{path}.paragraphs', paragraphs):
                for j, value in enumerate(paragraphs):
                    if not _text(value):
                        self.error(f'{path}.paragraphs[{j}]', 'deve ser texto não vazio')
            image_ids = section.get('imageIds', [])
            if self.lst(f'{path}.imageIds', image_ids):
                for j, ref in enumerate(image_ids):
                    self.image_ref(f'{path}.imageIds[{j}]', ref)
            artwork_ids = section.get('artworkIds', [])
            if self.lst(f'{path}.artworkIds', artwork_ids):
                for j, ref in enumerate(artwork_ids):
                    if not isinstance(ref, str) or ref not in self.artwork_ids:
                        self.error(f'{path}.artworkIds[{j}]', f'referência a obra inexistente: {ref!r}')
            links = section.get('links', [])
            if self.lst(f'{path}.links', links):
                for j, link in enumerate(links):
                    link_path = f'{path}.links[{j}]'
                    if not self.obj(link_path, link):
                        continue
                    if not _text(link.get('label')):
                        self.error(f'{link_path}.label', 'texto obrigatório')
                    href = link.get('href')
                    if not (_internal_path(href) or _https_url(href)):
                        self.error(f'{link_path}.href', 'deve ser um caminho interno (/...) ou um URL https://')

            if not any(section.get(k) for k in ('heading', 'paragraphs', 'imageIds', 'artworkIds', 'links')):
                self.warn(path, 'secção sem conteúdo; não será apresentada')

    # --- artist and artworks ---------------------------------------------------------

    def artist(self, artist):
        if artist is None or not self.obj('artist', artist):
            return
        self.no_unknown('artist', artist, ARTIST_FIELDS)
        if not _text(artist.get('name')):
            self.error('artist.name', 'nome obrigatório quando existe artista')
        for key in ('id', 'bio'):
            self.optional_text(f'artist.{key}', artist.get(key))
        if artist.get('portrait') is not None:
            self.image_ref('artist.portrait', artist['portrait'])
        website = artist.get('website')
        if website is not None and not _https_url(website):
            self.error('artist.website', 'deve ser null ou um URL https:// válido')

    def artworks(self, artworks, artist):
        if not self.lst('artworks', artworks):
            return
        ids = set()
        for i, work in enumerate(artworks):
            path = f'artworks[{i}]'
            if not self.obj(path, work):
                continue
            self.no_unknown(path, work, ARTWORK_FIELDS)
            work_id = work.get('id')
            if not _text(work_id):
                self.error(f'{path}.id', 'identificador obrigatório')
            elif work_id in ids:
                self.error(f'{path}.id', f'identificador repetido: {work_id!r}')
            else:
                ids.add(work_id)
            if not _text(work.get('artistId')):
                self.error(f'{path}.artistId', 'identificador do artista obrigatório')
            if not _text(work.get('title')):
                self.error(f'{path}.title', 'título obrigatório; não atribuir "Sem título" sem confirmação')
            for key in ('year', 'technique', 'dimensions', 'description'):
                self.optional_text(f'{path}.{key}', work.get(key))
            for key in ('imageId', 'fullImageId'):
                self.image_ref(f'{path}.{key}', work.get(key))
            if not _is_int(work.get('order')):
                self.error(f'{path}.order', 'deve ser um inteiro')
            if type(work.get('featured')) is not bool:
                self.error(f'{path}.featured', 'deve ser booleano')
        if artworks and artist is None:
            self.required_for_production('artist', 'identificação do artista obrigatória para publicar obras')

    # --- images ------------------------------------------------------------------------

    def images(self, images):
        if not self.obj('images', images):
            return
        for key, image in images.items():
            path = f'images.{key}'
            if not _text(key):
                self.error(path, 'ID de imagem vazio')
            if not self.obj(path, image):
                continue
            self.no_unknown(path, image, IMAGE_FIELDS)
            if image.get('id') != key:
                self.error(f'{path}.id', 'deve coincidir com a chave no manifesto de imagens')
            self.asset(f'{path}.src', image.get('src'))
            for dim in ('width', 'height'):
                if not _is_int(image.get(dim)) or image[dim] <= 0:
                    self.error(f'{path}.{dim}', 'deve ser um inteiro positivo')
            alt = image.get('alt')
            if alt is None:
                self.required_for_production(f'{path}.alt', 'texto alternativo obrigatório para produção '
                                                            '("" apenas para imagens decorativas)')
            elif not isinstance(alt, str):
                self.error(f'{path}.alt', 'deve ser texto')
            for name in ('caption', 'credit'):
                self.optional_text(f'{path}.{name}', image.get(name))

            variants = image.get('variants', [])
            if self.lst(f'{path}.variants', variants):
                for j, variant in enumerate(variants):
                    variant_path = f'{path}.variants[{j}]'
                    if not self.obj(variant_path, variant):
                        continue
                    self.asset(f'{variant_path}.src', variant.get('src'))
                    for dim in ('width', 'height'):
                        if not _is_int(variant.get(dim)) or variant[dim] <= 0:
                            self.error(f'{variant_path}.{dim}', 'deve ser um inteiro positivo')
                    if variant.get('mimeType') not in MIME_TYPES:
                        self.error(f'{variant_path}.mimeType', 'deve ser ' + ', '.join(MIME_TYPES))

            mobile = image.get('mobileImageId')
            if mobile is not None:
                if mobile == key:
                    self.error(f'{path}.mobileImageId', 'não pode referenciar a própria imagem')
                else:
                    self.image_ref(f'{path}.mobileImageId', mobile)

            focal = image.get('focalPoint')
            if focal is not None:
                if not isinstance(focal, dict) or set(focal) != {'x', 'y'}:
                    self.error(f'{path}.focalPoint', 'deve ser {x, y} ou null')
                else:
                    for axis in ('x', 'y'):
                        if not _is_number(focal[axis]) or not 0 <= focal[axis] <= 1:
                            self.error(f'{path}.focalPoint.{axis}', 'deve ser um número entre 0 e 1')

    def asset(self, path, value):
        if not _asset_path(value):
            self.error(path, 'deve ser um caminho local /assets/... sem "..", espaços ou parâmetros')
            return
        if self.public_dir is None:
            return
        target = (self.public_dir / value.lstrip('/')).resolve()
        if not target.is_relative_to(self.public_dir):
            self.error(path, 'o caminho sai da pasta pública')
        elif not target.is_file():
            self.required_for_production(path, f'ficheiro não encontrado na pasta pública: {value}')

    # --- navigation -----------------------------------------------------------------------

    def navigation(self, navigation):
        if not self.obj('navigation', navigation):
            return
        self.no_unknown('navigation', navigation, ('menuEnabled',))
        enabled = navigation.get('menuEnabled')
        if type(enabled) is not bool:
            self.error('navigation.menuEnabled', 'deve ser booleano')
        elif enabled:
            self.required_for_production('navigation.menuEnabled',
                                         'o menu de demonstração não pode ser publicado nesta fase')