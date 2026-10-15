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
            self.assertNotIn('href="/menu/"', html)
            self.assertNotIn('href="None"', html)
            self.assertNotIn('href=""', html)

    def test_unknown_contacts_are_not_invented(self):
        html = render_site(self.model)['reservas/index.html']
        self.assertNotIn('https://wa.me/', html)
        self.assertNotIn('mailto:', html)
        self.assertIn('ainda não recebe pedidos', html)

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
