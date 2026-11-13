import copy
import json
import tempfile
import unittest
from pathlib import Path
from urllib.parse import parse_qs, urlsplit

import support
from data_loader import ContentError, load_content
from normalizer import normalize_content


class LoaderTests(unittest.TestCase):
    def test_merges_site_and_pages(self):
        with tempfile.TemporaryDirectory() as tmp:
            Path(tmp, 'site.json').write_text(json.dumps({'name': 'X', 'preview': True}), encoding='utf-8')
            Path(tmp, 'pages.json').write_text(json.dumps({'home': support.page()}), encoding='utf-8')
            data = load_content(tmp)
        self.assertEqual(data['pages']['home']['title'], 'Página')

    def test_missing_and_invalid_files_raise_content_error(self):
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaisesRegex(ContentError, 'em falta'):
                load_content(tmp)
            Path(tmp, 'site.json').write_text('{"name": ', encoding='utf-8')
            with self.assertRaisesRegex(ContentError, 'JSON inválido.*linha 1'):
                load_content(tmp)

    def test_refuses_two_sources_for_pages(self):
        with tempfile.TemporaryDirectory() as tmp:
            Path(tmp, 'site.json').write_text(json.dumps({'pages': {}}), encoding='utf-8')
            Path(tmp, 'pages.json').write_text('{}', encoding='utf-8')
            with self.assertRaisesRegex(ContentError, 'única fonte'):
                load_content(tmp)

    def test_real_content_is_readable(self):
        data = load_content()
        self.assertEqual(set(data['pages']), set(support.PAGE_KEYS))


class NormalizerTests(unittest.TestCase):
    def test_does_not_mutate_source(self):
        source = support.complete_source()
        before = copy.deepcopy(source)
        normalize_content(source)
        self.assertEqual(source, before)

    def test_builds_encoded_contact_links(self):
        contacts = normalize_content(support.complete_source())['restaurant']['contacts']
        self.assertEqual(contacts['phoneHref'], 'tel:+351210000000')
        self.assertEqual(contacts['phoneDisplay'], '+351 210 000 000')
        wa = urlsplit(contacts['whatsappHref'])
        self.assertEqual((wa.scheme, wa.netloc, wa.path), ('https', 'wa.me', '/351910000000'))
        self.assertNotIn(' ', contacts['whatsappHref'])
        self.assertIn('%26', contacts['whatsappHref'])  # "&" must not split the query
        self.assertEqual(parse_qs(wa.query)['text'], ['Olá! Mesa para 2 & café?'])
        self.assertEqual(contacts['emailHref'], 'mailto:reservas@example.com?subject=Pedido%20de%20reserva')
        self.assertEqual(contacts['emailDisplay'], 'reservas@example.com')
        self.assertEqual(contacts['directionsHref'], 'https://maps.example.com/cachupa')

    def test_private_source_fields_do_not_reach_public_model(self):
        model = normalize_content(support.complete_source())
        self.assertNotIn('name', model)
        self.assertEqual(set(model['restaurant']), {'city', 'address', 'hours', 'contacts'})
        dumped = json.dumps(model)
        for private in ('whatsappNumber', 'whatsappMessage', 'emailSubject', 'directionsUrl', 'published'):
            self.assertNotIn(private, dumped)

    def test_unknown_values_become_null_not_placeholders(self):
        model = normalize_content({'name': ' ', 'restaurant': {'address': '  ', 'email': 'não é email'}})
        self.assertIsNone(model['site']['name'])
        self.assertIsNone(model['restaurant']['address'])
        self.assertEqual(model['restaurant']['hours'], [])
        self.assertEqual(model['pages'], {})  # missing pages are reported, never invented
        self.assertIsNone(model['restaurant']['contacts']['emailHref'])
        self.assertEqual(model['navigation'], {'menuEnabled': False})

    def test_artist_without_name_is_null(self):
        self.assertIsNone(normalize_content(support.complete_source())['artist'])

    def test_drafts_and_their_images_are_removed(self):
        source = support.complete_source()
        source['artist'] = {'name': 'Artista'}
        image = {'src': '/assets/photos/x.webp', 'width': 10, 'height': 10, 'alt': 'Obra'}
        source['images'] = {'public': dict(image, id='public'), 'draft': dict(image, id='draft'),
                            'unused': dict(image, id='unused')}
        source['artworks'] = [
            {'id': 'a1', 'artistId': 'x', 'title': 'Pública', 'imageId': 'public', 'order': 1, 'published': True},
            {'id': 'a2', 'artistId': 'x', 'title': 'Rascunho', 'imageId': 'draft', 'order': 2, 'published': False},
            {'id': 'a3', 'artistId': 'x', 'title': 'Sem estado', 'imageId': 'draft', 'order': 3},
        ]
        source['pages']['home']['sections'] = [
            {'id': 'art', 'type': 'artworkSelection', 'heading': 'Obras', 'artworkIds': ['a1', 'a2', 'a3']}]
        model = normalize_content(source)
        self.assertEqual([w['id'] for w in model['artworks']], ['a1'])
        self.assertEqual(model['artworks'][0]['fullImageId'], 'public')
        self.assertEqual(model['pages']['home']['sections'][0]['artworkIds'], ['a1'])
        self.assertEqual(set(model['images']), {'public'})

    def test_mobile_variant_of_referenced_image_is_kept(self):
        source = support.complete_source()
        source['images'] = {
            'hero': {'id': 'hero', 'src': '/assets/photos/a.webp', 'width': 1, 'height': 1,
                     'alt': '', 'mobileImageId': 'hero-m'},
            'hero-m': {'id': 'hero-m', 'src': '/assets/photos/b.webp', 'width': 1, 'height': 1, 'alt': ''},
        }
        source['pages']['home']['heroImageId'] = 'hero'
        model = normalize_content(source)
        self.assertEqual(set(model['images']), {'hero', 'hero-m'})
        self.assertEqual(model['images']['hero']['alt'], '')  # decorative alt is kept as ""

    def test_mode_sets_preview_flag(self):
        self.assertTrue(normalize_content(support.complete_source(), 'preview')['preview'])
        self.assertFalse(normalize_content(support.complete_source(), 'production')['preview'])
        with self.assertRaises(ValueError):
            normalize_content({}, 'staging')


if __name__ == '__main__':
    unittest.main()

