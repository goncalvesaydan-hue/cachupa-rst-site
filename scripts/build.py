"""Build the public site with Python's standard library. Never overwrites menu data."""
import json
import re
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
data = json.loads((ROOT / 'content/site.json').read_text())
def e(value): return escape(str(value), quote=True)
def local_image(value):
    if not isinstance(value, str) or not value.startswith('/assets/') or '..' in value:
        raise ValueError('As imagens da galeria devem usar caminhos locais /assets/.')
    if not (ROOT / value.lstrip('/')).is_file():
        raise ValueError(f'Imagem não encontrada: {value}')
    return e(value)

links = [('/', 'Início'), ('/menu/', 'Menu'), ('/a-nossa-casa/', 'A nossa casa'), ('/galeria/', 'Galeria'), ('/contactos/', 'Contactos'), ('/reservas/', 'Reservar mesa')]
def page(route, title, description, body):
    navigation = ''.join(f'<a href="{url}"'+ (' aria-current="page"' if url == route else '') + (' class="reserve"' if url == '/reservas/' else '') + f'>{label}</a>' for url, label in links)
    preview = '<div class="preview">Pré-visualização do site · Conteúdo em preparação</div>' if data['preview'] else ''
    html = f'''<!doctype html>
<html lang="pt-PT"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>{e(title)} — Cachupa Rst</title><meta name="description" content="{e(description)}"><meta name="theme-color" content="#006c9a">{'<meta name="robots" content="noindex, nofollow">' if data['preview'] else ''}<link rel="icon" href="/menu/brand/logo.svg" type="image/svg+xml"><link rel="stylesheet" href="/assets/site.css"><script src="/assets/site.js" defer></script></head>
<body><a class="skip" href="#main">Saltar para o conteúdo</a>{preview}<header class="header"><div class="wrap header-inner"><a class="logo" href="/" aria-label="Cachupa Rst — Início"><img src="/menu/brand/logo.svg" alt="Cachupa Rst Restaurante" width="1660" height="948"></a><button class="toggle" type="button" aria-expanded="false" aria-controls="site-nav">Navegação</button><nav class="nav" id="site-nav" aria-label="Navegação principal">{navigation}</nav></div></header><main id="main" tabindex="-1">{body}</main><footer class="footer"><div class="wrap"><div class="footer-top"><a href="/" aria-label="Cachupa Rst — Início"><img class="footer-logo" src="/menu/brand/logo.svg" alt="Cachupa Rst" width="1660" height="948"></a><div class="footer-links"><a href="/menu/">Menu</a><a href="/galeria/">Galeria</a><a href="/reservas/">Reservas</a><a href="/contactos/">Contactos</a></div></div><div class="footer-bottom"><span>Cachupa Rst · Cozinha cabo-verdiana</span><a href="/privacidade/">Privacidade</a></div></div></footer></body></html>'''
    destination = ROOT / (route.strip('/') + '/index.html' if route != '/' else 'index.html')
    if route == '/404': destination = ROOT / '404.html'
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(html)

def heading(title, intro):
    return f'<section class="page-heading"><div class="wrap"><a class="breadcrumb" href="/">Voltar ao início</a><h1>{e(title)}</h1><p>{e(intro)}</p></div></section>'

page('/', 'Cabo Verde, à mesa', 'Conheça o Cachupa Rst: cozinha cabo-verdiana, cachupa e arte. Consulte o menu e descubra a nossa casa.', '''
<section class="hero"><div class="wrap hero-grid"><div><h1>Cabo Verde,<br>à mesa.</h1><p>A cachupa dá o nome à casa. A cozinha e a cultura cabo-verdianas dão-lhe o lugar à mesa.</p><div class="actions"><a class="button yellow" href="/menu/">Ver o menu</a><a class="button outline" href="/a-nossa-casa/">Conhecer a casa</a></div></div><div class="brand-print"><img src="/menu/brand/logo.svg" alt="Cachupa Rst Restaurante" width="1660" height="948"><p class="hand">Puxe uma cadeira.</p><div class="print-line" aria-hidden="true"></div></div></div></section>
<div class="wrap welcome-strip"><span>Cozinha cabo-verdiana</span><span>Há lugar para a nossa cultura.</span></div>
<section class="section paper"><div class="wrap split"><div><h2>A nossa especialidade<br>tem nome de casa.</h2><p>A cachupa está no centro do nosso menu. Tradicional, vegetariana ou com diferentes acompanhamentos: conheça as versões que estamos a preparar para a carta.</p><a class="text-link" href="/menu/">Consultar o menu online</a></div><div><ul class="dish-list"><li>Cachupa tradicional</li><li>Cachupa vegetariana</li><li>Cachupa de bacalhau</li></ul><p class="note">Seleção da carta em preparação. O menu online mantém, por agora, os produtos de demonstração.</p></div></div></section>
<section class="section"><div class="wrap split"><h2>Uma casa<br>cabo-verdiana.</h2><div><p>À mesa, a cachupa. Nas paredes e no site, espaço para a pintura cabo-verdiana. Queremos que a visita também seja um encontro com a nossa cultura.</p><a class="text-link" href="/a-nossa-casa/">A nossa casa</a></div></div></section>
<section class="section art-teaser"><div class="wrap split"><div class="art-word" aria-hidden="true"><span>Arte</span><span>da terra.</span></div><div><h2>A cultura também<br>se vê.</h2><p>Uma galeria dedicada aos quadros de um pintor cabo-verdiano. Um espaço para olhar com tempo e conhecer quem está por detrás de cada obra.</p><div class="actions"><a class="button outline" href="/galeria/">Conhecer a galeria</a></div></div></div></section>
<section class="section"><div class="wrap visit"><div><h2>Até à mesa.</h2><p>Prepare a sua visita ao Cachupa Rst.</p></div><div class="actions"><a class="button" href="/reservas/">Reservas</a><a class="button outline" href="/contactos/">Contactos e localização</a></div></div></section>''')

page('/a-nossa-casa/', 'A nossa casa', 'Conheça a ligação do Cachupa Rst à cozinha e à cultura cabo-verdianas.', heading('A nossa casa.', 'Um restaurante de cozinha cabo-verdiana, com a cachupa no centro da mesa.') + '''<section class="section"><div class="wrap split"><h2>Da cozinha<br>à cultura.</h2><div class="text-column"><p>O Cachupa Rst nasce da vontade de dar espaço à cozinha cabo-verdiana. A nossa especialidade é a cachupa, que dá o nome ao restaurante e ocupa um lugar central no menu.</p><p>A pintura também fará parte desta experiência, numa galeria dedicada ao trabalho de um pintor cabo-verdiano.</p><div class="actions"><a class="button" href="/menu/">Ver o menu</a><a class="button outline" href="/galeria/">Visitar a galeria</a></div></div></div></section><section class="section paper"><div class="wrap status-block"><h2>A história, pelas nossas palavras.</h2><p>Em breve, vamos apresentar as pessoas, a história e as fotografias desta casa.</p></div></section>''')

artist = data['artist']
works = [work for work in data['artworks'] if work.get('published')]
if works:
    figures = []
    for work in works:
        image = local_image(work['image'])
        full = local_image(work.get('fullImage', work['image']))
        title = e(work['title'])
        metadata = ' · '.join(str(value) for value in [artist.get('name'), work.get('year'), work.get('technique'), work.get('dimensions'), work.get('credit')] if value)
        figures.append(f'<figure class="artwork"><button type="button" data-artwork data-full="{full}" aria-label="Ampliar: {title}"><img src="{image}" alt="{e(work["alt"])}" loading="lazy" width="600" height="480"></button><figcaption><h2>{title}</h2><p>{e(metadata)}</p></figcaption></figure>')
    gallery = '<div class="gallery-grid">' + ''.join(figures) + '</div><dialog id="art-dialog" class="art-dialog" aria-labelledby="art-title"><button class="dialog-close" type="button" autofocus>Fechar</button><img alt=""><h2 id="art-title"></h2><p></p></dialog>'
else:
    gallery = '<div class="gallery-empty"><div><h2>Estamos a preparar a exposição.</h2><p>Em breve, este espaço será preenchido com os quadros e a história do artista.</p><a class="text-link" href="/a-nossa-casa/">Conheça a nossa casa</a></div></div>'
artist_html = f'<section class="section paper"><div class="wrap split"><h2>{e(artist["name"])}</h2><p>{e(artist.get("bio") or "")}</p></div></section>' if artist.get('name') else ''
page('/galeria/', 'Galeria', 'Uma galeria dedicada à pintura de um artista cabo-verdiano, no Cachupa Rst.', heading('Um lugar para a arte.', 'Uma galeria inteiramente dedicada aos quadros de um pintor cabo-verdiano.') + '<section class="section"><div class="wrap">' + gallery + '</div></section>' + artist_html)

restaurant = data['restaurant']
phone = restaurant.get('phone')
phone_url = re.sub(r'[^+0-9]', '', phone or '')
phone_link = f'<a href="tel:{e(phone_url)}">{e(phone)}</a>' if phone_url else 'Contacto a disponibilizar.'
email = restaurant.get('email')
email_link = f'<a href="mailto:{e(email)}">{e(email)}</a>' if email and re.fullmatch(r'[^\s@]+@[^\s@]+\.[^\s@]+',email) else 'Email a disponibilizar.'
reservation_body = f'<h2>Fale connosco.</h2><p>Para pedir uma reserva, contacte o restaurante. A equipa confirma consigo a disponibilidade.</p><div class="actions"><a class="button" href="tel:{e(phone_url)}">Ligar para reservar</a></div>' if phone_url else '<h2>Reservas online em preparação.</h2><p>O canal de reservas estará disponível aqui em breve. Neste momento, este site ainda não recebe pedidos de reserva.</p><a class="text-link" href="/menu/">Consultar o menu</a>'
page('/reservas/', 'Reservas', 'Informação sobre reservas no Cachupa Rst.', heading('Vamos guardar-lhe lugar.', 'Planeie a sua próxima visita.') + f'<section class="section"><div class="wrap split"><div class="status-block">{reservation_body}</div><div><h2>À mesa, com tempo.</h2><p>Quando o contacto estiver disponível, indique o dia, a hora e o número de pessoas. A reserva fica confirmada depois da resposta da equipa.</p></div></div></section>')
hours = '<br>'.join(e(item) for item in restaurant.get('hours', [])) or 'Horários a confirmar.'
directions = restaurant.get('directionsUrl')
map_link = f'<a class="button" href="{e(directions)}" target="_blank" rel="noopener noreferrer">Como chegar</a>' if directions and directions.startswith('https://') else ''
page('/contactos/', 'Contactos', 'Contactos, localização e horários do Cachupa Rst.', heading('Encontre a nossa casa.', 'Morada, horários e formas de falar connosco.') + f'<section class="section"><div class="wrap split"><div><h2>Antes da visita.</h2><p>Estamos a preparar a informação de localização e contacto do restaurante.</p><div class="actions">{map_link}</div></div><dl class="contact-list"><div><dt>Morada</dt><dd>{e(restaurant.get("address") or "Morada a confirmar.")}</dd></div><div><dt>Horário</dt><dd>{hours}</dd></div><div><dt>Telefone</dt><dd>{phone_link}</dd></div><div><dt>Email</dt><dd>{email_link}</dd></div></dl></div></section>')
page('/privacidade/', 'Privacidade', 'Estado da informação de privacidade desta pré-visualização.', heading('Privacidade.', 'Informação sobre esta versão do site.') + '<section class="section"><div class="wrap text-column"><h2>Uma versão em preparação.</h2><p>Esta pré-visualização não inclui formulários de recolha de dados nem ferramentas de análise de visitas. O menu guarda no seu navegador a preferência de idioma.</p><h2>Antes da publicação.</h2><p>A informação de privacidade será completada com a identificação e o contacto do responsável e os serviços efetivamente utilizados, incluindo alojamento e reservas.</p></div></section>')
page('/404', 'Página não encontrada', 'Regresse ao site Cachupa Rst.', heading('Esta página não está aqui.', 'Pode regressar ao início ou consultar o menu.') + '<section class="section"><div class="wrap actions"><a class="button" href="/">Voltar ao início</a><a class="button outline" href="/menu/">Ver o menu</a></div></section>')
print('Geradas 7 páginas públicas e 404. Menu preservado.')
