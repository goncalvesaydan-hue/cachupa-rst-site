"""Presentation-only adapter. Gemini supplies a normalized contract-v1 model.

render_site(model) -> {relative output path: HTML}. No file writes or network I/O.
"""
from html import escape
from pathlib import Path
from string import Template
from urllib.parse import urlsplit, unquote

BASE = Template((Path(__file__).parent / 'templates/base.html').read_text())
ROUTES = {
    'home': ('/', 'index.html'),
    'house': ('/a-nossa-casa/', 'a-nossa-casa/index.html'),
    'gallery': ('/galeria/', 'galeria/index.html'),
    'reservations': ('/reservas/', 'reservas/index.html'),
    'contacts': ('/contactos/', 'contactos/index.html'),
    'privacy': ('/privacidade/', 'privacidade/index.html'),
    'notFound': ('/404.html', '404.html'),
}
DAYS = ['Segunda-feira', 'Terça-feira', 'Quarta-feira', 'Quinta-feira', 'Sexta-feira', 'Sábado', 'Domingo']


def text(value):
    return escape(str(value if value is not None else ''), quote=True)


def href(value, kind='link'):
    """Defense in depth; authoritative model validation belongs to backend."""
    if not isinstance(value, str) or not value or any(ord(c) < 32 for c in value):
        return ''
    if '\\' in value:
        return ''
    decoded = unquote(value)
    if any(ord(c) < 32 for c in decoded):
        return ''
    try:
        parsed = urlsplit(value)
        if kind == 'image':
            return value if value.startswith('/assets/') and '..' not in decoded.split('/') else ''
        if kind == 'whatsapp':
            return value if parsed.scheme == 'https' and parsed.netloc == 'wa.me' else ''
        if kind in ('email', 'phone'):
            return value if parsed.scheme == {'email': 'mailto', 'phone': 'tel'}[kind] else ''
        if value.startswith('/') and not value.startswith('//') and not decoded.startswith('//'):
            return value
        if parsed.scheme == 'https' and parsed.hostname and not parsed.username:
            return value
    except ValueError:
        pass
    return ''


def link(label, target, classes='', kind='link'):
    safe = href(target, kind)
    return f'<a class="{text(classes)}" href="{text(safe)}">{text(label)}</a>' if safe else ''


def paragraphs(values):
    return ''.join(f'<p>{text(p)}</p>' for p in values if p)


def placeholder(label, kind='pot'):
    # Images disabled for now.
    return ''


def image(model, image_id, *, hero=False, artwork=False):
    item = model['images'].get(image_id)
    if not item or not href(item.get('src'), 'image'):
        if artwork:
            return '<p class="image-error">Imagem da obra indisponível.</p>'
        return placeholder('Cachupa Rst') if model['preview'] else ''
    def sources(record, media=''):
        grouped = {}
        for variant in record.get('variants', []):
            if href(variant.get('src'), 'image') and isinstance(variant.get('width'), int) and variant['width'] > 0:
                grouped.setdefault(variant.get('mimeType'), []).append(variant)
        result = ''
        for mime, variants in grouped.items():
            if mime not in ('image/avif', 'image/webp', 'image/jpeg', 'image/png'):
                continue
            srcset = ', '.join(f'{text(v["src"])} {v["width"]}w' for v in sorted(variants, key=lambda v: v['width']))
            result += f'<source {media} type="{mime}" srcset="{srcset}" sizes="(max-width: 700px) 100vw, 70vw">'
        if media and not result:
            result = f'<source {media} srcset="{text(record["src"])}">'
        return result
    mobile = model['images'].get(item.get('mobileImageId')) if not artwork else None
    source_tags = sources(mobile, 'media="(max-width: 700px)"') if mobile and href(mobile.get('src'), 'image') else ''
    source_tags += sources(item)
    focal = item.get('focalPoint') if not artwork else None
    position = ''
    if focal and all(isinstance(focal.get(k), (int, float)) and 0 <= focal[k] <= 1 for k in ('x', 'y')):
        position = f' style="object-position:{focal["x"]*100}% {focal["y"]*100}%"'
    priority = 'loading="eager" fetchpriority="high"' if hero else 'loading="lazy"'
    cls = 'media media-art' if artwork else 'media'
    caption = ' · '.join(str(item[k]) for k in ('caption', 'credit') if item.get(k))
    return f'<figure class="{cls}"><picture>{source_tags}<img src="{text(item["src"])}" width="{int(item["width"])}" height="{int(item["height"])}" alt="{text(item.get("alt"))}" {priority} decoding="async"{position}></picture><span class="image-error" hidden>Imagem indisponível.</span>{"<figcaption>"+text(caption)+"</figcaption>" if caption else ""}</figure>'


def contact_actions(model, compact=False, hero=False):
    contacts = model['restaurant']['contacts']
    wa = link('Reservar por WhatsApp', contacts.get('whatsappHref'), 'button', 'whatsapp')
    email = link('Enviar email', contacts.get('emailHref'), 'button button-outline', 'email')
    if compact:
        label = 'Reservar mesa' if hero else 'Reservas'
        return wa or link(label, '/reservas/', 'button')
    return f'<div class="actions">{wa}{email}</div>' if wa or email else '<p class="status-note">Os contactos estarão disponíveis em breve. O site ainda não recebe pedidos de reserva.</p>'


def hours(model):
    rows = []
    for day in sorted(model['restaurant'].get('hours', []), key=lambda d: d['day']):
        intervals = ['%s–%s%s' % (v['opens'], v['closes'], ' (dia seguinte)' if v.get('closesNextDay') else '') for v in day['intervals']]
        value = 'Encerrado' if day['closed'] else ' / '.join(intervals)
        rows.append(f'<div><dt>{DAYS[day["day"]-1]}</dt><dd>{text(value)}{("<small>"+text(day["note"])+"</small>") if day.get("note") else ""}</dd></div>')
    return '<dl class="hours">' + ''.join(rows) + '</dl>' if rows else '<p class="muted">Horários a confirmar.</p>'


def contacts_panel(model):
    rest = model['restaurant']; c = rest['contacts']
    email = link(c.get('emailDisplay'), c.get('emailHref'), kind='email')
    copy = f'<button class="copy-button" type="button" data-copy-email="{text(c["emailDisplay"])}" hidden>Copiar email</button>' if c.get('emailDisplay') else ''
    return f'''<div class="contact-grid"><section><h2>Encontre-nos.</h2><p>{text(rest.get('address') or 'Morada a confirmar.')}</p><p>{text(rest.get('city'))}</p>{link('Como chegar', c.get('directionsHref'), 'text-link')}</section><section><h2>Fale connosco.</h2>{contact_actions(model)}<p>{text(c.get('whatsappDisplay'))}</p><div class="email-line">{email or text(c.get('emailDisplay') or 'Email a disponibilizar.')}{copy}</div><p>{link(c.get('phoneDisplay'), c.get('phoneHref'), kind='phone')}</p></section><section><h2>Horários.</h2>{hours(model)}</section></div>'''


def art_cards(model, selected=None):
    works = sorted(model['artworks'], key=lambda w: w['order'])
    if selected is not None:
        works = [w for w in works if w['id'] in selected]
    output = []
    for work in works:
        full = model['images'].get(work['fullImageId']) or model['images'].get(work['imageId'])
        metadata = ' · '.join(str(v) for v in [model['artist']['name'] if model.get('artist') else None, work.get('year'), work.get('technique'), work.get('dimensions')] if v)
        credit = full.get('credit') if full else None
        visual = image(model, work['imageId'], artwork=True)
        anchor = f'<a class="art-trigger" href="{text(href(full["src"], "image"))}" data-artwork aria-label="Ampliar: {text(work["title"])}">{visual}</a>' if full and href(full.get('src'), 'image') else visual
        output.append(f'<article class="art-card">{anchor}<h3>{text(work["title"])}</h3><p class="art-meta">{text(metadata)}</p><p class="art-description">{text(work.get("description"))}</p><p class="art-credit">{text(credit)}</p></article>')
    if not output:
        return '<div class="empty-gallery"><div class="empty-frame" aria-hidden="true"><span>Arte<br>da nossa<br>terra.</span></div><div><h3>A exposição está a ser preparada.</h3><p>Em breve, os quadros e a história do artista estarão aqui.</p></div></div>'
    return '<div class="art-grid">' + ''.join(output) + '</div>'


def sections(model, page):
    out = []
    for section in page['sections']:
        kind = section['type']
        if kind not in ('editorial', 'photoGrid', 'artworkSelection', 'visit'):
            raise ValueError('Unsupported section type: ' + kind)
        if not any(section.get(k) for k in ('heading', 'paragraphs', 'imageIds', 'artworkIds', 'links')):
            continue
        copy = (f'<h2>{text(section["heading"])}</h2>' if section.get('heading') else '') + paragraphs(section.get('paragraphs', []))
        actions = ''.join(link(v['label'], v['href'], 'text-link') for v in section.get('links', []))
        pictures = ''.join(image(model, ref) for ref in section.get('imageIds', []))
        if kind == 'artworkSelection':
            content = f'<div class="section-intro">{copy}{actions}</div>{art_cards(model, section.get("artworkIds", []))}'
        elif kind == 'photoGrid':
            content = f'<div class="section-intro">{copy}</div><div class="photo-grid">{pictures}</div>{actions}'
        elif kind == 'visit':
            content = f'<div class="visit-copy">{copy}{contact_actions(model)}{actions}</div><div>{pictures}{hours(model)}</div>'
        else:
            if not pictures and model['preview'] and page is not model['pages']['privacy']:
                pictures = placeholder(section.get('heading') or 'Fotografia da casa', 'house' if section['id'] in ('house', 'story') else 'pot')
            content = f'<div class="section-image">{pictures}</div><div class="section-copy">{copy}{actions}</div>'
        layout_class = ' text-only' if kind == 'editorial' and not pictures else ''
        out.append(f'<section class="section section-{kind}{layout_class}" id="{text(section["id"])}"><div class="shell section-layout">{content}</div></section>')
    return ''.join(out)


DIALOG = '''<dialog class="art-dialog" id="art-dialog" aria-labelledby="art-title"><div class="dialog-bar"><span id="art-position" role="status" aria-live="polite"></span><button type="button" data-art-close autofocus>Fechar</button></div><div class="dialog-image"><img alt=""><p class="image-error" hidden>Não foi possível carregar esta imagem.</p></div><div class="dialog-caption"><h2 id="art-title"></h2><p data-art-meta></p><p data-art-description></p><p data-art-credit></p></div><div class="dialog-navigation"><button type="button" data-art-prev>Anterior</button><button type="button" data-art-next>Seguinte</button></div></dialog>'''


def render_site(model):
    """Return complete static pages; do not normalize, persist or publish data."""
    if type(model.get('schemaVersion')) is not int or model['schemaVersion'] != 1:
        raise ValueError('Expected schemaVersion 1')
    if type(model.get('preview')) is not bool:
        raise ValueError('preview must be boolean')
    name = model['site']['name']
    rendered = {}
    for key, (route, output) in ROUTES.items():
        page = model['pages'][key]
        nav = [('/', 'Início'), ('/a-nossa-casa/', 'A nossa casa'), ('/galeria/', 'Galeria'), ('/contactos/', 'Contactos')]
        if model['navigation']['menuEnabled']:
            nav.insert(1, ('/menu/', 'Menu'))
        navigation = ''.join('<a href="' + url + '"' + (' aria-current="page"' if route == url else '') + '>' + label + '</a>' for url, label in nav) + contact_actions(model, compact=True)
        hero_image = image(model, page.get('heroImageId'), hero=True) if page.get('heroImageId') else ''
        if key in ('home', 'house') and not hero_image and model['preview']:
            hero_image = placeholder('Cachupa Rst', 'pot' if key == 'home' else 'house')
        home_actions = f'<div class="actions">{contact_actions(model, compact=True, hero=True)}{link("Conhecer a casa", "/a-nossa-casa/", "button button-outline")}</div>' if key == 'home' else ''
        breadcrumb = link('Início', '/', 'breadcrumb') if key != 'home' else '<p class="cuisine">Cozinha cabo-verdiana</p>'
        hero = f'<section class="page-hero {"home-hero" if key=="home" else ""} {"has-photo" if hero_image else ""} {"has-real-image" if page.get("heroImageId") in model["images"] else ""}"><div class="shell hero-layout"><div class="hero-copy">{breadcrumb}<h1>{text(page["heading"])}</h1>{paragraphs([page.get("intro")])}{home_actions}</div>{hero_image}</div></section>'
        ribbon = '<div class="identity-band"><span>Cozinha cabo-verdiana</span><span class="band-star" aria-hidden="true">✦</span><span>Cachupa Rst</span><span class="band-star" aria-hidden="true">✦</span><span>À mesa, em boa companhia.</span></div>' if key == 'home' else ''
        body = hero + ribbon + sections(model, page)
        if key == 'gallery':
            artist = model.get('artist')
            if artist:
                portrait = image(model, artist.get('portrait')) if artist.get('portrait') else ''
                body += f'<section class="section"><div class="shell artist">{portrait}<div><h2>{text(artist["name"])}</h2>{paragraphs([artist.get("bio")])}{link("Conhecer o artista",artist.get("website"),"text-link")}</div></div></section>'
            body += '<section class="section"><div class="shell">' + art_cards(model) + '</div></section>'
        if key == 'reservations':
            helper_html = '<div class="booking-helper" id="booking-helper" hidden><label class="helper-label">Personalizar pedido para o WhatsApp:</label><div class="helper-group"><span class="helper-title">Pessoas:</span><div class="helper-pills"><button type="button" class="helper-pill active" data-people="2">2 pessoas</button><button type="button" class="helper-pill" data-people="4">4 pessoas</button><button type="button" class="helper-pill" data-people="6">6 pessoas</button><button type="button" class="helper-pill" data-people="grupo">Grupo</button></div></div><div class="helper-group"><span class="helper-title">Refeição:</span><div class="helper-pills"><button type="button" class="helper-pill active" data-meal="Almoço">Almoço</button><button type="button" class="helper-pill" data-meal="Jantar">Jantar</button></div></div></div>'
            body += f'<section class="section"><div class="shell reservation-grid"><div><h2>Uma conversa, uma mesa.</h2><p>Indique o dia, a hora e o número de pessoas. A equipa confirma a disponibilidade consigo.</p>{helper_html}{contact_actions(model)}<p class="muted">O pedido só fica confirmado depois da resposta da equipa.</p></div><aside><h3>Antes de enviar</h3><ol><li>Abra a conversa no WhatsApp.</li><li>Complete os dados do pedido.</li><li>Envie a mensagem e aguarde a resposta.</li></ol><p>O site não envia mensagens automaticamente.</p></aside></div></section>'
        if key == 'contacts':
            body += '<section class="section"><div class="shell">' + contacts_panel(model) + '</div></section>'
        if key == 'notFound':
            body += '<div class="shell error-actions">' + link('Voltar ao início', '/', 'button') + '</div>'
        if 'data-artwork' in body:
            body += DIALOG
        metadata = '<meta name="robots" content="noindex, nofollow">' if model['preview'] else ''
        base = href(model['site'].get('baseUrl'))
        if base and base.startswith('https://'):
            canonical = base.rstrip('/') + route
            metadata += f'<link rel="canonical" href="{text(canonical)}"><meta property="og:url" content="{text(canonical)}">'
        metadata += f'<meta property="og:type" content="website"><meta property="og:title" content="{text(page["title"])}"><meta property="og:description" content="{text(page["description"])}">'
        c = model['restaurant']['contacts']
        footer_contacts = paragraphs([model['restaurant'].get('address')]) + link(c.get('emailDisplay'), c.get('emailHref'), kind='email') + ''.join(link(v['label'],v['href'],'social-link') for v in c.get('socialLinks',[]))
        rendered[output] = BASE.substitute(locale=text(model['site']['locale']), title=text(page['title']+' — '+name), description=text(page['description']), metadata=metadata, name=text(name), preview='<div class="preview">Pré-visualização · Fotografias selecionadas; contactos e créditos por confirmar</div>' if model['preview'] else '', navigation=navigation, body=body, footer_contacts=footer_contacts)
    return rendered
