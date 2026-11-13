import copy
import json
from pathlib import Path
import sys
import unittest
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))
from render import render_site, href, hours, image

class RendererTests(unittest.TestCase):
    def setUp(self):
        self.model = json.loads((ROOT / 'fixtures/preview.json').read_text())

    def test_routes_and_no_mutation(self):
        before = copy.deepcopy(self.model)
        pages = render_site(self.model)
        self.assertEqual(len(pages), 7)
        self.assertEqual(before, self.model)
        self.assertEqual(pages, render_site(self.model))
        for html in pages.values():
            self.assertEqual(html.count('<h1>'), 1)
            self.assertIn('noindex, nofollow', html)
            self.assertIn('href="/menu/"', html)
            self.assertNotIn('href="None"', html)
            self.assertNotIn('href=""', html)

    def test_menu_navigation_is_controlled_by_flag(self):
        pages = render_site(self.model)
        home = pages['index.html']
        self.assertEqual(home.count('href="/menu/"'), 2)
        footer_navigation = home.split('<nav aria-label="Navegação do rodapé">', 1)[1].split('</nav>', 1)[0]
        self.assertIn('<a href="/menu/">Menu</a>', footer_navigation)

        self.model['navigation']['menuEnabled'] = False
        for html in render_site(self.model).values():
            self.assertNotIn('href="/menu/"', html)

    def test_unknown_contacts_are_not_invented(self):
        html = render_site(self.model)['reservas/index.html']
        self.assertNotIn('https://wa.me/', html)
        self.assertNotIn('mailto:', html)
        self.assertNotIn('WhatsApp', html)
        self.assertIn('Os canais digitais de reserva não estão configurados.', html)
        self.assertNotIn('em breve', html.casefold())
        self.assertIn('Reservar', html)
        self.assertNotIn('data-people', html)
        self.assertNotIn('booking-helper', html)

    def test_email_only_reservations_do_not_claim_whatsapp(self):
        self.model['restaurant']['contacts'].update(emailDisplay='teste@example.invalid', emailHref='mailto:teste@example.invalid')
        pages = render_site(self.model)
        reservations = pages['reservas/index.html']
        home = pages['index.html']
        self.assertIn('Peça a sua reserva por email.', reservations)
        self.assertIn('mailto:teste@example.invalid', reservations)
        self.assertNotIn('WhatsApp', reservations)
        self.assertIn('Ver reservas', home)

    def test_home_uses_confirmed_copy_and_clear_navigation(self):
        pages = render_site(self.model)
        home = pages['index.html']
        self.assertIn('<h1>Cabo Verde,<br><em>à mesa.</em></h1>', home)
        self.assertIn('<span>Cachupa</span><b>RST</b>', home)
        self.assertIn('class="main-nav"', home)
        self.assertIn('class="menu-button"', home)
        self.assertRegex(home, r'<img [^>]+loading="eager" decoding="async" fetchpriority="high"')
        self.assertIn('Ver reservas', home)
        self.assertIn('<a class="nav-reserve" href="/reservas/">Reservar <span aria-hidden="true">↗</span></a>', home)
        hero = home.split('<section class="hero">', 1)[1].split('</section>', 1)[0]
        self.assertIn(self.model['pages']['home']['intro'], hero)
        self.assertIn('Conhecer a casa', hero)
        self.assertNotIn('12h00 às 23h00', home)

    def test_mobile_navigation_reservations_route_is_internal(self):
        html = render_site(self.model)['contactos/index.html']
        self.assertIn('<a class="nav-reserve" href="/reservas/">Reservar <span aria-hidden="true">↗</span></a>', html)
        self.assertIn('<a href="/contactos/" class="active" aria-current="page">Contactos</a>', html)

    def test_real_photos_and_artworks_placed_in_correct_slots(self):
        pages = render_site(self.model)
        home = pages['index.html']
        house = pages['a-nossa-casa/index.html']
        gallery = pages['galeria/index.html']
        contacts = pages['contactos/index.html']
        for photo in (
            '/assets/photos/hero-parede-quadro.jpg',
            '/assets/photos/studio-carne.jpg',
            '/assets/photos/studio-polvo.jpg',
            '/assets/photos/studio-refogada.jpg',
            '/assets/photos/studio-casa-quadro.jpg',
            '/assets/photos/studio-frango.jpg',
            '/assets/photos/arte-caldeirao.jpg',
            '/assets/photos/arte-serenata.jpg',
            '/assets/photos/arte-pescador.jpg',
        ):
            self.assertIn(photo, home)
        for photo in (
            '/assets/photos/studio-sala.jpg',
            '/assets/photos/studio-pintura-cachupa.jpg',
            '/assets/photos/studio-hero.jpg',
            '/assets/photos/studio-carne.jpg',
        ):
            self.assertIn(photo, house)
        self.assertEqual(gallery.count('data-artwork'), 11)
        self.assertIn('Onze obras', gallery)
        self.assertIn('/assets/photos/janela-1600.webp', contacts)

    def test_escaping_and_url_rejection(self):
        self.model['pages']['home']['heading'] = '<script>alert(1)</script>'
        html = render_site(self.model)['index.html']
        self.assertIn('&lt;script&gt;', html)
        self.assertNotIn('<script>alert', html)
        for url in ('javascript:alert(1)', '//evil.example', '/%2fevil.example', 'https://x\n.test', 'https://user@evil.example'):
            self.assertEqual(href(url), '')
        self.assertEqual(href('/assets/%2e%2e/private', 'image'), '')
        self.assertEqual(href('https://wa.me.evil.test/1', 'whatsapp'), '')

    def test_backend_contact_urls_are_preserved(self):
        c = self.model['restaurant']['contacts']
        c.update(emailDisplay='teste@example.invalid', emailHref='mailto:teste@example.invalid', whatsappHref='https://wa.me/123?text=Ol%C3%A1')
        html = render_site(self.model)['contactos/index.html']
        self.assertIn('https://wa.me/123?text=Ol%C3%A1', html)
        self.assertIn('mailto:teste@example.invalid', html)
        self.assertIn('data-copy-email="teste@example.invalid"', html)

    def test_overnight_hours(self):
        self.model['restaurant']['hours'] = [{'day': 5, 'closed': False, 'intervals': [{'opens': '19:00', 'closes': '01:00', 'closesNextDay': True}], 'note': None}]
        self.assertIn('19:00–01:00 (dia seguinte)', hours(self.model))

    def test_artwork_link_and_responsive_media(self):
        self.model['images']['sample'] = {'id': 'sample', 'src': '/assets/test.jpg', 'width': 800, 'height': 1000, 'alt': 'Quadro <teste>', 'credit': 'Autor', 'caption': None, 'variants': [{'src': '/assets/test.webp', 'width': 800, 'height': 1000, 'mimeType': 'image/webp'}], 'mobileImageId': None, 'focalPoint': {'x': .2, 'y': .4}}
        self.model['artworks'] = [{'id': 'test', 'artistId': 'a', 'title': 'Teste', 'year': None, 'technique': None, 'dimensions': None, 'description': 'Descrição', 'imageId': 'sample', 'fullImageId': 'sample', 'order': 0, 'featured': False}]
        html = render_site(self.model)['galeria/index.html']
        self.assertIn('href="/assets/test.jpg" data-artwork', html)
        self.assertIn('id="art-dialog"', html)
        self.assertIn('Quadro &lt;teste&gt;', html)
        self.assertIn('srcset="/assets/test.webp 800w"', html)
        self.assertNotIn('object-position', image(self.model, 'sample', artwork=True))
        self.assertIn('fetchpriority="high"', image(self.model, 'sample', hero=True))
        self.assertIn('loading="lazy" decoding="async"', image(self.model, 'sample'))

    def test_empty_contacts_are_factual_and_not_repeated(self):
        empty = copy.deepcopy(self.model)
        empty['restaurant']['city'] = None
        empty['restaurant']['address'] = None
        empty['restaurant']['hours'] = []
        empty['restaurant']['contacts'] = {
            'phoneDisplay': None,
            'phoneHref': None,
            'whatsappDisplay': None,
            'whatsappHref': None,
            'emailDisplay': None,
            'emailHref': None,
            'directionsHref': None,
            'socialLinks': [],
        }
        html = render_site(empty)['contactos/index.html']
        self.assertIn('Contactos por confirmar.', html)
        self.assertIn('Morada por confirmar.', html)
        self.assertIn('Horários por confirmar.', html)
        self.assertNotIn('a disponibilizar', html)
        self.assertNotIn('em breve', html.casefold())
        self.assertIn('Consultar contactos', html)
        self.assertNotIn('Horários e localização', html)

    def test_confirmed_contacts_address_and_hours(self):
        html = render_site(self.model)['contactos/index.html']
        self.assertIn('R. Alm. Reis 22 B, 2830-326 Barreiro', html)
        self.assertIn('Barreiro', html)
        self.assertIn('963 572 411', html)
        self.assertIn('tel:+351963572411', html)
        self.assertIn('11:00–23:00', html)
        self.assertIn('https://www.google.com/maps/search/?api=1&amp;query=Restaurante+Cachupa+Brr', html)

    def test_invalid_contact_links_still_show_the_confirmed_display_value(self):
        self.model['restaurant']['contacts'].update(phoneDisplay='+351 210 000 000', phoneHref='javascript:alert(1)')
        html = render_site(self.model)['contactos/index.html']
        self.assertIn('+351 210 000 000', html)
        self.assertNotIn('href="javascript:alert(1)"', html)

    def test_contract_version_rejected(self):
        self.model['schemaVersion'] = 2
        with self.assertRaises(ValueError):
            render_site(self.model)

    def test_production_has_no_preview_banner(self):
        self.model['preview'] = False
        html = render_site(self.model)['index.html']
        self.assertNotIn('noindex, nofollow', html)
        self.assertNotIn('Fotografia por adicionar', html)

if __name__ == '__main__':
    unittest.main()
