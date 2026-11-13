"""Turn the editorial source (content/) into the public contract-v1 model.

The normalizer only shapes structure and derives links. It never invents content:
unknown values become null or [] and wrongly typed values are passed through so the
validator can report them with their field path. It does not fill gaps with
placeholders, default titles or fake image sizes.

Private/legacy source fields (phone, email, whatsappNumber, whatsappMessage,
emailSubject, directionsUrl, published) are consumed here and never reach the
public model. Draft artworks and images that nothing references are dropped.
"""
import copy
import re
from urllib.parse import quote

MODES = ('preview', 'production')
CONTACT_FIELDS = (
    'phoneDisplay', 'phoneHref', 'whatsappDisplay', 'whatsappHref',
    'emailDisplay', 'emailHref', 'directionsHref',
)
_EMAIL = re.compile(r'[^\s@<>"\'?&]+@[^\s@<>"\'?&]+\.[^\s@<>"\'?&]+')


def normalize_content(source, mode='preview'):
    """Return a new public model; `source` is never mutated."""
    if mode not in MODES:
        raise ValueError(f'modo desconhecido: {mode!r}')
    src = copy.deepcopy(source) if isinstance(source, dict) else {}

    artworks, draft_ids = _artworks(src.get('artworks'))
    model = {
        'schemaVersion': src.get('schemaVersion', 1),
        'preview': mode == 'preview',
        'site': _site(src),
        'restaurant': _restaurant(src.get('restaurant')),
        'pages': _pages(src.get('pages'), draft_ids),
        'artist': _artist(src.get('artist')),
        'artworks': artworks,
        'images': {},
        'navigation': _navigation(src.get('navigation')),
    }
    model['images'] = _images(src.get('images'), _referenced_image_ids(model))
    return model


def _clean(value):
    """Trim text; empty text means unknown (null). Other types pass through."""
    if isinstance(value, str):
        return value.strip() or None
    return value


def _obj(value):
    return value if isinstance(value, dict) else {}


# --- site ------------------------------------------------------------------

def _site(src):
    site = _obj(src.get('site'))
    return {
        # Legacy sources keep the name at the root.
        'name': _clean(site.get('name')) or _clean(src.get('name')),
        'locale': site.get('locale', 'pt-PT'),
        'baseUrl': _clean(site.get('baseUrl')),
    }


# --- restaurant and contacts -------------------------------------------------

def _restaurant(value):
    restaurant = _obj(value)
    return {
        'city': _clean(restaurant.get('city')),
        'address': _clean(restaurant.get('address')),
        'hours': _hours(restaurant.get('hours')),
        'contacts': _contacts(restaurant),
    }


def _hours(value):
    if value is None:
        return []
    if not isinstance(value, list):
        return value
    result = []
    for day in value:
        if not isinstance(day, dict):
            result.append(day)
            continue
        intervals = day.get('intervals', [])
        if isinstance(intervals, list):
            intervals = [
                {
                    'opens': item.get('opens'),
                    'closes': item.get('closes'),
                    'closesNextDay': item.get('closesNextDay', False),
                } if isinstance(item, dict) else item
                for item in intervals
            ]
        result.append({
            'day': day.get('day'),
            'closed': day.get('closed'),
            'intervals': intervals,
            'note': _clean(day.get('note')),
        })
    return result


def _contacts(restaurant):
    source = _obj(restaurant.get('contacts'))
    contacts = {field: _clean(source.get(field)) for field in CONTACT_FIELDS}

    # Telephone: display text from the source; tel: link derived from its digits.
    phone = contacts['phoneDisplay'] or _clean(restaurant.get('phone'))
    if isinstance(phone, str):
        contacts['phoneDisplay'] = phone
        if contacts['phoneHref'] is None:
            contacts['phoneHref'] = _tel_href(phone)

    # WhatsApp: number + optional message become one wa.me link (contract §Contactos).
    number = _clean(restaurant.get('whatsappNumber')) or contacts['whatsappDisplay']
    if isinstance(number, str):
        contacts['whatsappDisplay'] = contacts['whatsappDisplay'] or number
        if contacts['whatsappHref'] is None:
            contacts['whatsappHref'] = _whatsapp_href(number, _clean(restaurant.get('whatsappMessage')))

    # Email: display is the bare address (used by "copiar email"); mailto may carry a subject.
    email = contacts['emailDisplay'] or _clean(restaurant.get('email'))
    if isinstance(email, str):
        contacts['emailDisplay'] = email
        if contacts['emailHref'] is None and _EMAIL.fullmatch(email):
            subject = _clean(restaurant.get('emailSubject'))
            contacts['emailHref'] = 'mailto:' + email + (
                '?subject=' + quote(subject, safe='') if isinstance(subject, str) else ''
            )

    if contacts['directionsHref'] is None:
        contacts['directionsHref'] = _clean(restaurant.get('directionsUrl'))

    links = source.get('socialLinks', [])
    if isinstance(links, list):
        links = [
            {'label': _clean(link.get('label')), 'href': _clean(link.get('href'))}
            if isinstance(link, dict) else link
            for link in links
        ]
    contacts['socialLinks'] = links
    return contacts


def _tel_href(display):
    digits = re.sub(r'\D', '', display)
    if display.lstrip().startswith('00'):
        digits, plus = digits[2:], '+'
    else:
        plus = '+' if display.lstrip().startswith('+') else ''
    # Too short to be dialled: leave null; the validator reports the mismatch.
    return f'tel:{plus}{digits}' if len(digits) >= 6 else None


def _whatsapp_href(number, message):
    digits = re.sub(r'\D', '', number)
    if number.lstrip().startswith('00'):
        digits = digits[2:]
    if len(digits) < 8:
        return None
    href = f'https://wa.me/{digits}'
    if isinstance(message, str):
        href += '?text=' + quote(message, safe='')
    return href


# --- pages -------------------------------------------------------------------

def _pages(value, draft_ids):
    if not isinstance(value, dict):
        return {}
    pages = {}
    for key, page in value.items():
        if not isinstance(page, dict):
            pages[key] = page
            continue
        sections = page.get('sections', [])
        if isinstance(sections, list):
            sections = [_section(section, draft_ids) for section in sections]
        pages[key] = {
            'title': _clean(page.get('title')),
            'description': _clean(page.get('description')),
            'heading': _clean(page.get('heading')),
            'intro': _clean(page.get('intro')),
            'heroImageId': _clean(page.get('heroImageId')),
            'sections': sections,
        }
    return pages


def _section(section, draft_ids):
    if not isinstance(section, dict):
        return section
    paragraphs = section.get('paragraphs', [])
    if isinstance(paragraphs, list):
        paragraphs = [_clean(p) for p in paragraphs if _clean(p) is not None]
    links = section.get('links', [])
    if isinstance(links, list):
        links = [
            {'label': _clean(link.get('label')), 'href': _clean(link.get('href'))}
            if isinstance(link, dict) else link
            for link in links
        ]
    artwork_ids = section.get('artworkIds', [])
    if isinstance(artwork_ids, list):
        # Drafts must not leak to the browser, not even by ID.
        artwork_ids = [ref for ref in artwork_ids if not (isinstance(ref, str) and ref in draft_ids)]
    return {
        'id': _clean(section.get('id')),
        'type': section.get('type'),
        'heading': _clean(section.get('heading')),
        'paragraphs': paragraphs,
        'imageIds': section.get('imageIds', []),
        'artworkIds': artwork_ids,
        'links': links,
    }


# --- artist and artworks -------------------------------------------------------

def _artist(value):
    if value is None:
        return None
    if not isinstance(value, dict):
        return value
    name = _clean(value.get('name'))
    if name is None:
        # No identified artist yet: the contract allows artist = null.
        return None
    return {
        'id': _clean(value.get('id')),
        'name': name,
        'bio': _clean(value.get('bio')),
        'portrait': _clean(value.get('portrait')),
        'website': _clean(value.get('website')),
    }


def _artworks(value):
    """Return (public artworks, IDs of drafts removed)."""
    if value is None:
        return [], set()
    if not isinstance(value, list):
        return value, set()
    public, drafts = [], set()
    for work in value:
        if not isinstance(work, dict):
            public.append(work)
            continue
        # Only an explicit `published: true` is public (same rule as the legacy generator).
        if work.get('published') is not True:
            if isinstance(work.get('id'), str):
                drafts.add(work['id'])
            continue
        image_id = _clean(work.get('imageId'))
        public.append({
            'id': _clean(work.get('id')),
            'artistId': _clean(work.get('artistId')),
            'title': _clean(work.get('title')),
            'year': _clean(work.get('year')),
            'technique': _clean(work.get('technique')),
            'dimensions': _clean(work.get('dimensions')),
            'description': _clean(work.get('description')),
            'imageId': image_id,
            'fullImageId': _clean(work.get('fullImageId')) or image_id,
            'order': work.get('order'),
            'featured': work.get('featured', False),
        })
    return public, drafts


# --- images ----------------------------------------------------------------------

def _referenced_image_ids(model):
    refs = set()
    pages = model['pages'] if isinstance(model['pages'], dict) else {}
    for page in pages.values():
        if not isinstance(page, dict):
            continue
        refs.add(page.get('heroImageId'))
        for section in page['sections'] if isinstance(page.get('sections'), list) else []:
            if isinstance(section, dict) and isinstance(section.get('imageIds'), list):
                refs.update(ref for ref in section['imageIds'] if isinstance(ref, str))
    for work in model['artworks'] if isinstance(model['artworks'], list) else []:
        if isinstance(work, dict):
            refs.update((work.get('imageId'), work.get('fullImageId')))
    if isinstance(model['artist'], dict):
        refs.add(model['artist'].get('portrait'))
    return {ref for ref in refs if isinstance(ref, str)}


def _images(value, referenced):
    """Keep only referenced images (and their mobile variants) so unused or
    draft-only images are not published."""
    if value is None:
        return {}
    if not isinstance(value, dict):
        return value
    keep, pending = set(), list(referenced)
    while pending:
        ref = pending.pop()
        if ref in keep:
            continue
        keep.add(ref)
        mobile = _obj(value.get(ref)).get('mobileImageId')
        if isinstance(mobile, str):
            pending.append(mobile)
    return {key: _image(key, image) for key, image in value.items() if key in keep}


def _image(key, image):
    if not isinstance(image, dict):
        return image
    alt = image.get('alt')
    variants = image.get('variants', [])
    if isinstance(variants, list):
        variants = [
            {k: variant.get(k) for k in ('src', 'width', 'height', 'mimeType')}
            if isinstance(variant, dict) else variant
            for variant in variants
        ]
    return {
        'id': image.get('id', key),
        'src': _clean(image.get('src')),
        'width': image.get('width'),
        'height': image.get('height'),
        # An empty alt is meaningful (decorative image), so it is not turned into null.
        'alt': alt.strip() if isinstance(alt, str) else alt,
        'caption': _clean(image.get('caption')),
        'credit': _clean(image.get('credit')),
        'variants': variants,
        'mobileImageId': _clean(image.get('mobileImageId')),
        'focalPoint': image.get('focalPoint'),
    }


# --- navigation --------------------------------------------------------------------

def _navigation(value):
    return {'menuEnabled': _obj(value).get('menuEnabled', False)}