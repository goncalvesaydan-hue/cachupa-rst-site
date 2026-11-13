"""Presentation-only adapter. Gemini supplies a normalized contract-v1 model.

render_site(model) -> {relative output path: HTML}. No file writes or network I/O.
"""
from hashlib import sha256
from html import escape
from pathlib import Path
from string import Template
from urllib.parse import urlsplit, unquote

_SRC_DIR = Path(__file__).parent
BASE = Template((_SRC_DIR / 'templates/base.html').read_text())


def _compute_asset_version():
    digest = sha256()
    for rel in ('styles/site.css', 'scripts/site.js'):
        p = _SRC_DIR / rel
        if p.is_file():
            digest.update(p.read_bytes())
    return digest.hexdigest()[:8]


ASSET_VERSION = _compute_asset_version()
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
TRANSPARENT_PIXEL = 'data:image/gif;base64,R0lGODlhAQABAAAAACwAAAAAAQABAAA='

HEADING_ACCENTS = {
    'Cabo Verde, à mesa.': 'Cabo Verde,<br><em>à mesa.</em>',
    'As nossas especialidades.': 'As nossas<br><em>especialidades.</em>',
    'Novidades & Avisos da Casa': 'Novidades &amp;<br>Avisos da Casa',
    'Conheça a nossa casa.': 'Conheça a<br>nossa casa.',
    'Um lugar para a pintura.': 'Um lugar para<br><em>a pintura.</em>',
    'Puxe uma cadeira.': 'Puxe uma<br><em>cadeira.</em>',
    'À mesa, na nossa casa.': 'À mesa, na<br>nossa casa.',
    'Do tacho ao prato.': 'Do tacho<br><em>ao prato.</em>',
    'Esta página não está aqui.': 'Esta página<br><em>não está aqui.</em>',
}

DISH_TITLES = {
    'studio-polvo': 'Mar & lume brando',
    'studio-refogada': 'O clássico da casa',
}

NUMBER_WORDS = {
    1: 'Uma',
    2: 'Duas',
    3: 'Três',
    4: 'Quatro',
    5: 'Cinco',
    6: 'Seis',
    7: 'Sete',
    8: 'Oito',
    9: 'Nove',
    10: 'Dez',
    11: 'Onze',
    12: 'Doze',
}


def text(value):
    return escape(str(value if value is not None else ''), quote=True)


def styled_heading(value):
    raw = str(value if value is not None else '')
    return HEADING_ACCENTS.get(raw, text(raw))


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


def link(label, target, classes='', kind='link', arrow=False):
    safe = href(target, kind)
    if not safe or not label:
        return ''
    cls_attr = f' class="{text(classes)}"' if classes else ''
    ext_attr = ' target="_blank" rel="noopener noreferrer"' if safe.startswith('https://') else ''
    arrow_html = ' <span aria-hidden="true">↗</span>' if arrow else ''
    return f'<a{cls_attr} href="{text(safe)}"{ext_attr}>{text(label)}{arrow_html}</a>'


def paragraphs(values):
    return ''.join(f'<p>{text(p)}</p>' for p in values if p)


def placeholder(label='', frame_cls=''):
    cls = f'placeholder {frame_cls}'.strip()
    aria = f'Espaço reservado para: {label}' if label else 'Espaço reservado para imagem'
    return f'<figure class="{text(cls)}" aria-label="{text(aria)}"><span aria-hidden="true">Espaço reservado</span></figure>'


def image(model, image_id, *, hero=False, artwork=False, show_caption=True, frame_cls=''):
    item = model['images'].get(image_id)
    if not item or not href(item.get('src'), 'image'):
        if artwork:
            return (
                placeholder(str(image_id or 'obra'), frame_cls)
                if model['preview']
                else '<p class="image-error">Imagem da obra indisponível.</p>'
            )
        return placeholder(model['site'].get('name') or 'imagem', frame_cls) if model['preview'] else ''

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
            media_attr = f'{media} ' if media else ''
            result += f'<source {media_attr}type="{mime}" srcset="{srcset}" sizes="(max-width: 850px) 92vw, 55vw">'
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
    priority = ' fetchpriority="high"' if hero else ''
    loading = 'eager' if hero else 'lazy'
    cls_parts = ['media', 'media-art' if artwork else 'media-photo']
    if frame_cls:
        cls_parts.append(frame_cls)
    cls = ' '.join(cls_parts)
    raw_caption = item.get('caption') or (item.get('credit') if item.get('credit') != model['site'].get('name') else '')
    caption = str(raw_caption) if (show_caption and raw_caption) else ''
    figcaption_html = f'<figcaption class="caption">{text(caption)}</figcaption>' if caption else ''
    return (
        f'<figure class="{text(cls)}">'
        f'<div class="media-frame">'
        f'<picture>{source_tags}<img src="{text(item["src"])}" width="{int(item["width"])}" height="{int(item["height"])}" '
        f'alt="{text(item.get("alt"))}" loading="{loading}" decoding="async"{priority}{position}></picture>'
        f'<span class="image-error" hidden>Imagem indisponível.</span>'
        f'</div>'
        f'{figcaption_html}'
        f'</figure>'
    )


def image_caption(model, image_id):
    item = model['images'].get(image_id)
    if not item:
        return ''
    raw_caption = item.get('caption') or (item.get('credit') if item.get('credit') != model['site'].get('name') else '')
    return str(raw_caption) if raw_caption else ''


def reservation_channels(model):
    contacts = model['restaurant']['contacts']
    channels = []
    if href(contacts.get('whatsappHref'), 'whatsapp'):
        channels.append('WhatsApp')
    if href(contacts.get('emailHref'), 'email'):
        channels.append('email')
    return channels


def primary_booking_cta(model, *, fallback_label='Ver reservas', wa_label='Reservar mesa'):
    c = model['restaurant']['contacts']
    wa = href(c.get('whatsappHref'), 'whatsapp')
    if wa:
        return link(wa_label, wa, 'button', 'whatsapp', arrow=True)
    return link(fallback_label, '/reservas/', 'button', arrow=True)


def hours_summary(model):
    schedule = sorted(model['restaurant'].get('hours', []), key=lambda d: d['day'])
    if not schedule:
        return None
    open_days = [d for d in schedule if not d.get('closed') and d.get('intervals')]
    if not open_days:
        return None
    first_intervals = [
        '%s—%s%s' % (v['opens'], v['closes'], ' (+1)' if v.get('closesNextDay') else '')
        for v in open_days[0]['intervals']
    ]
    all_same = len(open_days) == 7 and all(
        d['intervals'] == open_days[0]['intervals'] for d in open_days
    )
    if all_same:
        v = open_days[0]['intervals'][0]
        return {
            'hero_days': 'Todos os dias',
            'hero_hours': ' / '.join(first_intervals),
            'footer_days': 'Segunda a Domingo',
            'footer_hours': f'{v["opens"]} às {v["closes"]}' if len(open_days[0]['intervals']) == 1 else ' / '.join(first_intervals),
        }
    return {
        'hero_days': 'Horário da casa',
        'hero_hours': ' / '.join(first_intervals),
        'footer_days': f'{len(open_days)} dias por semana',
        'footer_hours': ' / '.join(first_intervals),
    }


def hours(model):
    rows = []
    for day in sorted(model['restaurant'].get('hours', []), key=lambda d: d['day']):
        intervals = [
            '%s–%s%s' % (v['opens'], v['closes'], ' (dia seguinte)' if v.get('closesNextDay') else '')
            for v in day['intervals']
        ]
        value = 'Encerrado' if day['closed'] else ' / '.join(intervals)
        note_html = f' <small>({text(day["note"])})</small>' if day.get('note') else ''
        rows.append(f'<div class="hours-row"><dt>{DAYS[day["day"]-1]}</dt><dd>{text(value)}{note_html}</dd></div>')
    return '<dl class="hours">' + ''.join(rows) + '</dl>' if rows else '<p class="muted">Horários por confirmar.</p>'


def contacts_panel(model, page):
    rest = model['restaurant']
    c = rest['contacts']
    raw_address = rest.get('address')
    if raw_address and ',' in raw_address:
        first, second = [part.strip() for part in raw_address.split(',', 1)]
        address_html = f'<span class="address-line" aria-hidden="true">{text(first)},<br>{text(second)}</span>'
        sr_address = f'<span class="sr-only">{text(raw_address)}</span>'
        location_heading = f'<h2>{address_html}{sr_address}</h2>'
    else:
        location_heading = f'<h2>{text(raw_address or "Morada por confirmar.")}</h2>'

    city = rest.get('city')
    if city == 'Barreiro':
        city_html = '<p>Barreiro · Margem Sul · Portugal</p>'
    elif city:
        city_html = f'<p>{text(city)}</p>'
    else:
        city_html = ''

    directions = link('Abrir no Google Maps', c.get('directionsHref'), 'button', arrow=True)
    visual_id = page.get('heroImageId')
    location_visual = ''
    if visual_id and visual_id in model['images']:
        location_visual = image(model, visual_id, show_caption=True, frame_cls='map-space')
    elif model['preview'] and raw_address:
        location_visual = placeholder('montra e localização', 'map-space')

    direct_parts = []
    phone_display = c.get('phoneDisplay')
    phone_safe = href(c.get('phoneHref'), 'phone')
    if phone_safe:
        direct_parts.append(f'<a class="phone" href="{text(phone_safe)}">{text(phone_display or phone_safe)}</a>')
    elif phone_display:
        direct_parts.append(f'<p class="phone">{text(phone_display)}</p>')

    wa_link = link('Pedir por WhatsApp', c.get('whatsappHref'), 'text-link', 'whatsapp', arrow=True)
    if wa_link:
        direct_parts.append(f'<div>{wa_link}</div>')

    email_display = c.get('emailDisplay')
    email_safe = href(c.get('emailHref'), 'email')
    if email_safe or email_display:
        email_val = (
            link(email_display or 'Enviar email', c.get('emailHref'), 'text-link', 'email', arrow=True)
            if email_safe
            else f'<p class="contact-plain">{text(email_display)}</p>'
        )
        copy_btn = (
            f'<button class="copy-button" type="button" data-copy-email="{text(email_display)}" hidden>Copiar email</button>'
            if email_display else ''
        )
        direct_parts.append(f'<div class="email-row">{email_val}{copy_btn}</div>')

    direct_content = ''.join(direct_parts) if direct_parts else '<p class="status-note">Contactos por confirmar.</p>'

    return (
        f'<section class="contact-grid">'
        f'<div class="contact-location">'
        f'<p class="eyebrow">Localização</p>'
        f'{location_heading}'
        f'{city_html}'
        f'{directions}'
        f'{location_visual}'
        f'</div>'
        f'<div class="contact-details">'
        f'<div><p class="eyebrow">Contacto direto</p>{direct_content}</div>'
        f'<div class="schedule"><p class="eyebrow">Horário semanal</p>{hours(model)}</div>'
        f'</div>'
        f'</section>'
    )


def art_cards(model, selected=None, *, preview_mode=False):
    works = sorted(model['artworks'], key=lambda w: w['order'])
    if selected is not None:
        order_lookup = {art_id: idx for idx, art_id in enumerate(selected)}
        works = sorted(
            [w for w in works if w['id'] in order_lookup],
            key=lambda w: order_lookup[w['id']],
        )
    output = []
    artist_name = model['artist']['name'] if model.get('artist') and model['artist'].get('name') else None
    for idx, work in enumerate(works):
        full = model['images'].get(work['fullImageId']) or model['images'].get(work['imageId'])
        credit = full.get('credit') if full else None
        metadata = ' · '.join(
            str(v) for v in [
                artist_name,
                work.get('year'),
                work.get('dimensions'),
                credit,
            ] if v
        )
        if preview_mode:
            subtitle = ' · '.join(str(v) for v in [artist_name, work.get('technique')] if v)
            frame_cls = f'art-{idx + 1}'
            card_cls = 'art-card'
            number_html = ''
        else:
            subtitle = str(work.get('technique') or artist_name or '')
            frame_cls = ''
            card_cls = f'artwork artwork-{(idx % 4) + 1}'
            number_html = f'<span class="art-number">{idx + 1:02d}</span>'

        visual = image(model, work['imageId'], artwork=True, show_caption=False, frame_cls=frame_cls)
        subtitle_html = f'<small>{text(subtitle)}</small>' if subtitle else ''
        meta_block = (
            f'<span class="art-meta">'
            f'<strong>{text(work["title"])}</strong>'
            f'{subtitle_html}'
            f'</span>'
        )
        inner = f'{visual}{number_html}{meta_block}'
        if full and href(full.get('src'), 'image'):
            trigger = (
                f'<a class="art-trigger" href="{text(href(full["src"], "image"))}" data-artwork '
                f'aria-label="Ampliar: {text(work["title"])}">{inner}</a>'
            )
        else:
            trigger = f'<div class="art-trigger">{inner}</div>'

        output.append(
            f'<article class="{card_cls}">'
            f'{trigger}'
            f'<div class="art-detail-source" hidden>'
            f'<span class="art-title-source">{text(work["title"])}</span>'
            f'<span class="art-technique">{text(work.get("technique"))}</span>'
            f'<p class="art-description">{text(work.get("description"))}</p>'
            f'<p class="art-meta-line">{text(metadata)}</p>'
            f'<p class="art-credit">{text(credit)}</p>'
            f'</div>'
            f'</article>'
        )
    if not output:
        return (
            '<div class="empty-gallery">'
            '<h3>A exposição está a ser preparada.</h3>'
            '<p>As obras e a informação do artista serão apresentadas quando estiverem confirmadas.</p>'
            '</div>'
        )
    grid_cls = 'preview-grid' if preview_mode else 'art-grid'
    return f'<div class="{grid_cls}">' + ''.join(output) + '</div>'


def section_links_html(section, channels, cls='text-link'):
    items = []
    for v in section.get('links', []):
        label = (
            'Ver reservas'
            if v['href'] == '/reservas/' and 'whatsapp' in v['label'].casefold() and 'WhatsApp' not in channels
            else v['label']
        )
        rendered = link(label, v['href'], cls, arrow=True)
        if rendered:
            items.append(rendered)
    return ''.join(items)


def sections(model, page):
    out = []
    channels = reservation_channels(model)
    city = model['restaurant'].get('city')
    for section in page['sections']:
        kind = section['type']
        if kind not in ('editorial', 'photoGrid', 'artworkSelection', 'visit'):
            raise ValueError('Unsupported section type: ' + kind)
        if not any(section.get(k) for k in ('heading', 'paragraphs', 'imageIds', 'artworkIds', 'links')):
            continue
        sec_id = section.get('id', '')
        raw_heading = section.get('heading') or ''
        heading_html = f'<h2>{styled_heading(raw_heading)}</h2>' if raw_heading else ''
        copy_paragraphs = paragraphs(section.get('paragraphs', []))
        actions = section_links_html(section, channels, 'text-link')
        image_ids = section.get('imageIds', [])

        if kind == 'artworkSelection':
            eyebrow = f'<p class="eyebrow">Galeria {text(model["site"]["name"])}</p>'
            out.append(
                f'<section class="section gallery-preview" id="{text(sec_id)}">'
                f'<div class="section-heading">'
                f'<div>{eyebrow}{heading_html}</div>'
                f'<div>{copy_paragraphs}{actions}</div>'
                f'</div>'
                f'{art_cards(model, section.get("artworkIds", []), preview_mode=True)}'
                f'</section>'
            )
        elif kind == 'photoGrid':
            is_kitchen = sec_id == 'cozinha'
            eyebrow_text = 'Cozinha tradicional' if is_kitchen else 'Sabores da casa'
            sec_cls = 'section kitchen' if is_kitchen else 'section specialties'
            grid_cls = 'kitchen-grid' if is_kitchen else 'specialty-grid'
            cards = []
            for idx, img_id in enumerate(image_ids):
                frame_cls = 'landscape' if idx == 0 else ('portrait-short' if is_kitchen else 'square')
                pic = image(model, img_id, show_caption=False, frame_cls=frame_cls)
                cap = image_caption(model, img_id)
                cap_html = f'<p class="caption">{text(cap)}</p>' if cap else ''
                dish_title = DISH_TITLES.get(img_id, '') if not is_kitchen else ''
                title_html = f'<h3>{text(dish_title)}</h3>' if dish_title else ''
                if pic or title_html or cap_html:
                    cards.append(f'<div>{pic}{title_html}{cap_html}</div>')
            grid_html = f'<div class="{grid_cls}">{"".join(cards)}</div>' if cards else ''
            right_col = f'<div>{copy_paragraphs}{actions}</div>' if actions else copy_paragraphs
            out.append(
                f'<section class="{sec_cls}" id="{text(sec_id)}">'
                f'<div class="section-heading">'
                f'<div><p class="eyebrow">{eyebrow_text}</p>{heading_html}</div>'
                f'{right_col}'
                f'</div>'
                f'{grid_html}'
                f'</section>'
            )
        elif kind == 'visit':
            eyebrow_text = 'Rua Almirante Reis · Barreiro' if city == 'Barreiro' else 'Visite-nos'
            first_img = image_ids[0] if image_ids else None
            visual_html = (
                image(model, first_img, show_caption=False, frame_cls='visit-visual')
                if first_img else (placeholder('prato da casa', 'visit-visual') if model['preview'] else '')
            )
            cap = image_caption(model, first_img) if first_img else ''
            cap_html = f'<p class="caption visit-caption">{text(cap)}</p>' if cap else ''
            secondary_links = ''.join(
                link(v['label'], v['href'], 'button button--secondary')
                for v in section.get('links', [])
            )
            primary_btn = primary_booking_cta(model, fallback_label='Ver reservas', wa_label='Reservar mesa')
            out.append(
                f'<section class="visit" id="{text(sec_id)}">'
                f'{visual_html}'
                f'<div class="visit-copy">'
                f'<p class="eyebrow">{eyebrow_text}</p>'
                f'{heading_html}'
                f'{copy_paragraphs}'
                f'<div class="actions">{primary_btn}{secondary_links}</div>'
                f'</div>'
                f'{cap_html}'
                f'</section>'
            )
        else:
            if sec_id in ('noticias', 'news', 'novidades'):
                items = []
                for idx, p in enumerate(section.get('paragraphs', []), start=1):
                    badge = 'Nota'
                    title = ''
                    desc = p
                    if '—' in p:
                        badge, rest = [x.strip() for x in p.split('—', 1)]
                        badge = badge.lstrip('✦ ').strip()
                        if ':' in rest:
                            title, desc = [x.strip() for x in rest.split(':', 1)]
                        else:
                            title = rest
                    elif ':' in p:
                        title, desc = [x.strip() for x in p.split(':', 1)]
                    title_html = f'<h3>{text(title)}</h3>' if title else ''
                    items.append(
                        f'<article>'
                        f'<span>{idx:02d}</span>'
                        f'<div><p class="eyebrow">{text(badge)}</p>{title_html}</div>'
                        f'<p>{text(desc)}</p>'
                        f'</article>'
                    )
                out.append(
                    f'<section class="news section" id="{text(sec_id)}">'
                    f'<div class="news-title">'
                    f'<div><p class="eyebrow">À mesa, agora</p>{heading_html}</div>'
                    f'{actions}'
                    f'</div>'
                    f'<div class="news-list">{"".join(items)}</div>'
                    f'</section>'
                )
            elif sec_id == 'house':
                eyebrow_text = 'Uma casa no Barreiro' if city == 'Barreiro' else 'A nossa casa'
                first_img = image_ids[0] if image_ids else None
                visual_html = (
                    image(model, first_img, show_caption=False, frame_cls='tall')
                    if first_img else (placeholder('ambiente da sala', 'tall') if model['preview'] else '')
                )
                quote = '<blockquote>Sente-se.<br><em>Há lugar à mesa.</em></blockquote>'
                panel_cls = 'section house-panel' if visual_html else 'section'
                out.append(
                    f'<section class="{panel_cls}" id="{text(sec_id)}">'
                    f'<div class="copy-block">'
                    f'<p class="eyebrow">{eyebrow_text}</p>'
                    f'{heading_html}'
                    f'{copy_paragraphs}'
                    f'{quote}'
                    f'{actions}'
                    f'</div>'
                    f'{visual_html}'
                    f'</section>'
                )
            else:
                eyebrow_map = {
                    'speciality': 'O prato que dá nome à casa',
                    'story': 'História & ambiente',
                }
                eyebrow_val = eyebrow_map.get(sec_id, '')
                eyebrow_html = f'<p class="eyebrow">{text(eyebrow_val)}</p>' if eyebrow_val else ''
                quote_html = (
                    '<blockquote>Comida, arte<br><em>e hospitalidade.</em></blockquote>'
                    if sec_id == 'story' else ''
                )
                first_img = image_ids[0] if image_ids else None
                if first_img:
                    frame_cls = 'painting-natural' if 'pintura' in first_img else 'portrait'
                    visual_html = f'<div>{image(model, first_img, show_caption=True, frame_cls=frame_cls)}</div>'
                    sec_cls = 'section split'
                elif model['preview'] and sec_id in ('speciality', 'story'):
                    visual_html = f'<div>{placeholder(raw_heading, "portrait")}</div>'
                    sec_cls = 'section split'
                else:
                    visual_html = ''
                    sec_cls = 'section'
                out.append(
                    f'<section class="{sec_cls}" id="{text(sec_id)}">'
                    f'{visual_html}'
                    f'<div class="copy-block">{eyebrow_html}{heading_html}{copy_paragraphs}{quote_html}{actions}</div>'
                    f'</section>'
                )
    return ''.join(out)


def legal_page_body(page, channels):
    secs = [
        s for s in page['sections']
        if any(s.get(k) for k in ('heading', 'paragraphs', 'links'))
    ]
    if not secs:
        return ''
    nav_items = []
    articles = []
    for idx, sec in enumerate(secs, start=1):
        sec_id = sec.get('id') or f'legal-{idx}'
        heading = sec.get('heading') or f'Secção {idx}'
        nav_items.append(f'<a href="#{text(sec_id)}">{text(heading)}</a>')
        links_html = section_links_html(sec, channels, '')
        links_wrap = f'<div class="inline-links">{links_html}</div>' if links_html else ''
        articles.append(
            f'<article id="{text(sec_id)}">'
            f'<h2>{text(heading)}</h2>'
            f'{paragraphs(sec.get("paragraphs", []))}'
            f'{links_wrap}'
            f'</article>'
        )
    return (
        f'<section class="legal-layout">'
        f'<aside><p>Nesta página</p>{"".join(nav_items)}</aside>'
        f'<div class="legal-content">{"".join(articles)}</div>'
        f'</section>'
    )


def reservations_body(model):
    c = model['restaurant']['contacts']
    digital = reservation_channels(model)
    channel_rows = []
    step_channels = []

    wa_safe = href(c.get('whatsappHref'), 'whatsapp')
    if wa_safe:
        step_channels.append('WhatsApp')
        channel_rows.append(
            f'<a href="{text(wa_safe)}" target="_blank" rel="noopener noreferrer">'
            f'<span>{len(channel_rows) + 1:02d}</span>'
            f'<div><small>Canal recomendado</small><strong>WhatsApp</strong></div>'
            f'<span aria-hidden="true">↗</span>'
            f'</a>'
        )

    email_safe = href(c.get('emailHref'), 'email')
    if email_safe:
        step_channels.append('email')
        channel_rows.append(
            f'<a href="{text(email_safe)}">'
            f'<span>{len(channel_rows) + 1:02d}</span>'
            f'<div><small>Correio eletrónico</small><strong>{text(c.get("emailDisplay") or "Enviar email")}</strong></div>'
            f'<span aria-hidden="true">↗</span>'
            f'</a>'
        )

    phone_safe = href(c.get('phoneHref'), 'phone')
    phone_display = c.get('phoneDisplay')
    if phone_safe:
        step_channels.append('telefone')
        channel_rows.append(
            f'<a href="{text(phone_safe)}">'
            f'<span>{len(channel_rows) + 1:02d}</span>'
            f'<div><small>Telefone</small><strong>{text(phone_display or phone_safe)}</strong></div>'
            f'<span aria-hidden="true">↗</span>'
            f'</a>'
        )
    elif phone_display:
        step_channels.append('telefone')
        channel_rows.append(
            f'<div class="channel-muted">'
            f'<span>{len(channel_rows) + 1:02d}</span>'
            f'<div><small>Telefone</small><strong>{text(phone_display)}</strong></div>'
            f'</div>'
        )

    if not channel_rows:
        channel_rows.append(
            '<div class="channel-muted">'
            '<span>01</span>'
            '<div><small>Estado</small><strong>Não há contactos para reservas configurados.</strong></div>'
            '</div>'
        )

    digital_note = (
        ''
        if digital
        else '<p class="status-note">Os canais digitais de reserva não estão configurados.</p>'
    )

    if step_channels:
        if len(step_channels) == 1:
            via_text = step_channels[0]
        else:
            via_text = ', '.join(step_channels[:-1]) + ' ou ' + step_channels[-1]
        steps_list = [
            f'Contacte a equipa por {via_text}.',
            'Indique o dia, a hora e o número de pessoas.',
            'Aguarde a resposta da equipa para confirmar.',
        ]
    else:
        steps_list = [
            'Consulte os contactos confirmados junto da casa.',
            'Indique o dia, a hora e o número de pessoas.',
            'Aguarde a resposta da equipa para confirmar.',
        ]

    steps_cards = ''.join(
        f'<article><span>{idx:02d}</span><p>{text(step)}</p></article>'
        for idx, step in enumerate(steps_list, start=1)
    )

    return (
        f'<section class="reservation-panel">'
        f'<div class="reservation-intro">'
        f'<p class="eyebrow">Contacto direto</p>'
        f'<h2>Uma conversa,<br><em>uma mesa.</em></h2>'
        f'<p>Fale diretamente com a equipa para pedir uma reserva. A disponibilidade é confirmada na conversa.</p>'
        f'{digital_note}'
        f'</div>'
        f'<div class="channels">{"".join(channel_rows)}</div>'
        f'</section>'
        f'<section class="section steps">'
        f'<p class="eyebrow">Como pedir</p>'
        f'<div class="steps-grid">{steps_cards}</div>'
        f'<div class="notice"><strong>Importante</strong>'
        f'<p>O pedido só fica confirmado depois da resposta da equipa. Este site não envia mensagens nem confirma reservas.</p>'
        f'</div>'
        f'</section>'
    )


def brand_wordmark_html(name):
    parts = str(name or '').strip().split()
    if len(parts) >= 2 and parts[-1].casefold() == 'rst':
        main_part = ' '.join(parts[:-1])
        return f'<span>{text(main_part)}</span><b>{text(parts[-1].upper())}</b>'
    return f'<span>{text(name)}</span>'


def artist_initials(name):
    tokens = [part for part in str(name or '').split() if part]
    if not tokens:
        return ''
    if len(tokens) == 1:
        return tokens[0][:2].upper()
    return (tokens[0][0] + tokens[-1][0]).upper()


DIALOG = (
    f'<dialog class="art-dialog" id="art-dialog" closedby="any" aria-labelledby="art-title">'
    f'<div class="modal-layout">'
    f'<button class="modal-close" type="button" data-art-close autofocus>Fechar <span aria-hidden="true">×</span></button>'
    f'<div class="modal-visual">'
    f'<div class="modal-frame">'
    f'<img src="{TRANSPARENT_PIXEL}" alt="" fetchpriority="low">'
    f'<p class="image-error" hidden>Não foi possível carregar esta imagem.</p>'
    f'</div>'
    f'</div>'
    f'<div class="modal-copy">'
    f'<p class="eyebrow" id="art-position" role="status" aria-live="polite"></p>'
    f'<h2 id="art-title">Pintura em exposição</h2>'
    f'<p class="technique" data-art-technique></p>'
    f'<p class="modal-description" data-art-description></p>'
    f'<small data-art-meta></small>'
    f'<div class="modal-nav">'
    f'<button type="button" data-art-prev>← Anterior</button>'
    f'<button type="button" data-art-next>Seguinte →</button>'
    f'</div>'
    f'</div>'
    f'</div>'
    f'</dialog>'
)


def render_site(model):
    """Return complete static pages; do not normalize, persist or publish data."""
    if type(model.get('schemaVersion')) is not int or model['schemaVersion'] != 1:
        raise ValueError('Expected schemaVersion 1')
    if type(model.get('preview')) is not bool:
        raise ValueError('preview must be boolean')
    name = model['site']['name']
    rendered = {}
    channels = reservation_channels(model)
    summary_hours = hours_summary(model)
    city = model['restaurant'].get('city')
    artist = model.get('artist')

    for key, (route, output) in ROUTES.items():
        page = model['pages'][key]
        nav = [('/', 'Início'), ('/a-nossa-casa/', 'A nossa casa'), ('/galeria/', 'Galeria'), ('/contactos/', 'Contactos')]
        if model['navigation']['menuEnabled']:
            nav.insert(1, ('/menu/', 'Menu'))
        footer_menu_link = link('Menu', '/menu/') if model['navigation']['menuEnabled'] else ''
        nav_links = ''.join(
            f'<a href="{url}"'
            + (' class="active" aria-current="page"' if route == url else '')
            + f'>{label}</a>'
            for url, label in nav
        )
        reserve_cls = 'nav-reserve active' if route == '/reservas/' else 'nav-reserve'
        reserve_current = ' aria-current="page"' if route == '/reservas/' else ''
        navigation = (
            nav_links
            + f'<a class="{reserve_cls}" href="/reservas/"{reserve_current}>Reservar <span aria-hidden="true">↗</span></a>'
        )
        raw_heading = str(page.get('heading') or '')
        heading_inner = styled_heading(raw_heading)

        if key == 'home':
            hero_eyebrow = f'{text(city)} · Cozinha de Cabo Verde' if city else 'Cozinha de Cabo Verde'
            hero_visual = (
                image(model, page.get('heroImageId'), hero=True, show_caption=False, frame_cls='hero-visual')
                if page.get('heroImageId')
                else (placeholder('imagem principal do restaurante', 'hero-visual') if model['preview'] else '')
            )
            hero_note = (
                f'<p class="hero-note">{text(summary_hours["hero_days"])}<br><strong>{text(summary_hours["hero_hours"])}</strong></p>'
                if summary_hours else ''
            )
            primary_btn = primary_booking_cta(model, fallback_label='Ver reservas', wa_label='Reservar mesa')
            secondary_btn = link('Conhecer a casa', '/a-nossa-casa/', 'button button--secondary')
            body = (
                f'<section class="hero">'
                f'<div class="hero-copy">'
                f'<p class="eyebrow">{hero_eyebrow}</p>'
                f'<h1>{heading_inner}</h1>'
                f'{paragraphs([page.get("intro")])}'
                f'<div class="actions">{primary_btn}{secondary_btn}</div>'
                f'</div>'
                f'{hero_visual}'
                f'{hero_note}'
                f'</section>'
                + sections(model, page)
            )
        elif key == 'notFound':
            home_btn = link('Voltar ao início', '/', 'button', arrow=True)
            body = (
                f'<section class="not-found">'
                f'<p class="eyebrow">Erro 404</p>'
                f'<h1>{heading_inner}</h1>'
                f'{paragraphs([page.get("intro")])}'
                f'{home_btn}'
                f'</section>'
            )
        else:
            eyebrows = {
                'house': 'A nossa casa',
                'gallery': f'Galeria · {artist["name"]}' if artist and artist.get('name') else 'Galeria',
                'reservations': 'Reservas',
                'contacts': 'Contactos',
                'privacy': 'Legal & transparência',
            }
            hero_intro = page.get('intro')
            if key == 'reservations' and 'WhatsApp' not in channels:
                hero_intro = (
                    'Peça a sua reserva por email. A equipa confirma a disponibilidade consigo.'
                    if 'email' in channels
                    else 'Os canais de reserva estão indisponíveis nesta pré-visualização.'
                )
            show_hero_visual = key != 'contacts' and (
                bool(page.get('heroImageId')) or (key == 'house' and model['preview'] and bool(model['images']))
            )
            hero_visual = ''
            if show_hero_visual:
                hero_visual = (
                    image(model, page.get('heroImageId'), hero=True, show_caption=False, frame_cls='page-hero-visual')
                    if page.get('heroImageId')
                    else placeholder('ambiente da sala', 'page-hero-visual')
                )
            hero_cls = 'page-hero has-visual' if hero_visual else 'page-hero'
            hero = (
                f'<section class="{hero_cls}">'
                f'<div>'
                f'<p class="eyebrow">{text(eyebrows.get(key, page["title"]))}</p>'
                f'<h1>{heading_inner}</h1>'
                f'{paragraphs([hero_intro])}'
                f'</div>'
                f'{hero_visual}'
                f'</section>'
            )

            if key == 'privacy':
                body = hero + legal_page_body(page, channels)
            else:
                body = hero + sections(model, page)

            if key == 'house':
                invite_btn = primary_booking_cta(model, fallback_label='Ver reservas', wa_label='Reservar mesa')
                body += (
                    f'<section class="statement">'
                    f'<p class="eyebrow">O nosso convite</p>'
                    f'<p>Uma casa faz-se de quem chega,<br>de quem fica e de quem volta.</p>'
                    f'{invite_btn}'
                    f'</section>'
                )

            if key == 'gallery':
                if artist and artist.get('name'):
                    if artist.get('portrait') and artist.get('portrait') in model['images']:
                        badge_html = f'<div class="artist-portrait">{image(model, artist["portrait"], show_caption=False)}</div>'
                    else:
                        badge_html = f'<span aria-hidden="true">{text(artist_initials(artist["name"]))}</span>'
                    artist_web = link('Conhecer o artista', artist.get('website'), 'text-link', arrow=True)
                    body += (
                        f'<section class="artist-intro">'
                        f'{badge_html}'
                        f'<div>'
                        f'<p class="eyebrow">O artista</p>'
                        f'<h2>{text(artist["name"])}</h2>'
                        f'{paragraphs([artist.get("bio")])}'
                        f'{artist_web}'
                        f'</div>'
                        f'</section>'
                    )
                count = len(model['artworks'])
                if count:
                    word = NUMBER_WORDS.get(count, str(count))
                    plural = 'obra' if count == 1 else 'obras'
                    orig = 'original.' if count == 1 else 'originais.'
                    ex_heading = f'<h2>{text(word)} {plural}<br><em>{orig}</em></h2>'
                    ex_intro = '<p>Selecione uma obra para abrir a respetiva ficha completa.</p>'
                else:
                    ex_heading = '<h2>Exposição<br><em>na sala.</em></h2>'
                    ex_intro = ''
                body += (
                    f'<section class="section exhibition">'
                    f'<div class="exhibition-title">'
                    f'<p class="eyebrow">Exposição permanente</p>'
                    f'{ex_heading}'
                    f'{ex_intro}'
                    f'</div>'
                    f'{art_cards(model, preview_mode=False)}'
                    f'</section>'
                )

            if key == 'reservations':
                body += reservations_body(model)

            if key == 'contacts':
                body += contacts_panel(model, page)

        if 'data-artwork' in body:
            body += DIALOG

        metadata = '<meta name="robots" content="noindex, nofollow">' if model['preview'] else ''
        base = href(model['site'].get('baseUrl'))
        if base and base.startswith('https://'):
            canonical = base.rstrip('/') + route
            metadata += f'<link rel="canonical" href="{text(canonical)}"><meta property="og:url" content="{text(canonical)}">'
        description = page['description']
        if key == 'reservations' and 'WhatsApp' not in channels:
            description = (
                'Contactos para reservas indisponíveis.'
                if not channels
                else 'Peça a sua reserva por email; a equipa confirma a disponibilidade.'
            )
        metadata += (
            f'<meta property="og:type" content="website">'
            f'<meta property="og:title" content="{text(page["title"])}">'
            f'<meta property="og:description" content="{text(description)}">'
        )

        rest = model['restaurant']
        c = rest['contacts']
        if summary_hours:
            footer_schedule = (
                f'<p>{text(summary_hours["footer_days"])}<br>'
                f'<strong>{text(summary_hours["footer_hours"])}</strong></p>'
            )
        else:
            footer_schedule = '<p>Consulte os horários atualizados na página de contactos.</p>'

        footer_features = (
            '<ul class="plain-list">'
            '<li>Cozinha em serviço contínuo</li>'
            '<li>Esplanada &amp; sala acolhedora</li>'
            '<li>Opções vegetarianas &amp; veganas</li>'
            '<li>Noites com música ao vivo</li>'
            '</ul>'
            if (city == 'Barreiro' or summary_hours) else ''
        )
        footer_visit = footer_schedule + footer_features

        raw_addr = rest.get('address')
        if raw_addr and ',' in raw_addr:
            addr_a, addr_b = [part.strip() for part in raw_addr.split(',', 1)]
            addr_html = f'<address>{text(addr_a)}<br>{text(addr_b)}</address>'
        elif raw_addr:
            addr_html = f'<address>{text(raw_addr)}</address>'
        else:
            addr_html = ''

        maps_label = 'Restaurante Cachupa Brr no Google Maps' if city == 'Barreiro' else 'Abrir localização no Google Maps'
        contact_bits = (
            addr_html
            + link(c.get('phoneDisplay'), c.get('phoneHref'), kind='phone')
            + link(c.get('emailDisplay'), c.get('emailHref'), kind='email')
            + ''.join(link(v['label'], v['href'], arrow=True) for v in c.get('socialLinks', []))
            + link(maps_label, c.get('directionsHref'), arrow=True)
        )
        if not contact_bits:
            footer_contacts = link('Consultar contactos', '/contactos/')
        else:
            footer_contacts = contact_bits + link('Pedir reserva de mesa', '/reservas/', arrow=True)

        footer_summary = (
            'Acolhimento autêntico no Barreiro, com paredes de pedra rústica, cachupa confecionada ao lume brando e galeria viva de pintura original.'
            if city == 'Barreiro'
            else 'Cozinha tradicional de Cabo Verde com cachupa confecionada ao lume brando e acolhimento familiar à mesa.'
        )
        footer_art_credit = (
            f'<p>Obras de arte originais em exposição da autoria de {text(artist["name"])}.</p>'
            if artist and artist.get('name') else ''
        )
        if city == 'Barreiro':
            footer_location = '<p>Barreiro · Margem Sul · Portugal</p>'
        elif city:
            footer_location = f'<p>{text(city)}</p>'
        else:
            footer_location = ''

        wa_target = href(c.get('whatsappHref'), 'whatsapp') or '/reservas/'
        phone_target = href(c.get('phoneHref'), 'phone') or '/contactos/'
        directions_target = href(c.get('directionsHref'))
        mobile_secondary_target = directions_target or phone_target
        mobile_secondary_label = 'Como chegar' if directions_target else text(c.get('phoneDisplay') or 'Contactos')
        mobile_secondary_arrow = ' <span aria-hidden="true">↗</span>' if directions_target else ''
        mobile_primary_label = 'Reservar mesa' if href(c.get('whatsappHref'), 'whatsapp') else 'Ver reservas'
        mobile_primary_ext = ' target="_blank" rel="noopener noreferrer"' if wa_target.startswith('https://') else ''
        mobile_secondary_ext = ' target="_blank" rel="noopener noreferrer"' if mobile_secondary_target.startswith('https://') else ''
        mobile_buttons = []
        if wa_target != route:
            mobile_buttons.append(
                f'<a class="mobile-bar-primary" href="{text(wa_target)}"{mobile_primary_ext}>{mobile_primary_label}</a>'
            )
        if mobile_secondary_target != route:
            mobile_buttons.append(
                f'<a class="mobile-bar-secondary" href="{text(mobile_secondary_target)}"{mobile_secondary_ext}>{mobile_secondary_label}{mobile_secondary_arrow}</a>'
            )
        mobile_bar = (
            f'<nav class="mobile-bar" aria-label="Ações rápidas">{"".join(mobile_buttons)}</nav>'
            if mobile_buttons else ''
        )
        preview_banner = (
            '<div class="preview">Pré-visualização · Fotografias selecionadas; contactos digitais por confirmar</div>'
            if model['preview'] else ''
        )
        rendered[output] = BASE.substitute(
            locale=text(model['site']['locale']),
            title=text(page['title'] + ' — ' + name),
            description=text(description),
            metadata=metadata,
            asset_version=ASSET_VERSION,
            name=text(name),
            brand_wordmark=brand_wordmark_html(name),
            preview=preview_banner,
            navigation=navigation,
            body=body,
            footer_summary=text(footer_summary),
            footer_visit=footer_visit,
            footer_contacts=footer_contacts,
            footer_menu_link=footer_menu_link,
            footer_art_credit=footer_art_credit,
            footer_location=footer_location,
            mobile_bar=mobile_bar,
        )
    return rendered
