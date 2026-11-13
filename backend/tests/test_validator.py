import tempfile
import unittest
from pathlib import Path

import support
from data_loader import load_content
from normalizer import normalize_content
from validator import validate_model


def paths(issues):
    return {issue.path for issue in issues}


class ValidatorTests(unittest.TestCase):
    def model(self, mode='production', **changes):
        model = normalize_content(support.complete_source(), mode)
        model.update(changes)
        return model

    def test_complete_model_is_valid_in_both_modes(self):
        for mode in ('preview', 'production'):
            report = validate_model(self.model(mode), mode)
            self.assertEqual(report.errors, [], mode)

    def test_real_content_preview_passes_with_honest_warnings(self):
        model = normalize_content(load_content(), 'preview')
        report = validate_model(model, 'preview', public_dir=support.ROOT / 'frontend' / 'public')
        self.assertEqual(report.errors, [])
        self.assertIn('restaurant.contacts.whatsappHref', paths(report.warnings))

    def test_real_content_is_blocked_in_production(self):
        model = normalize_content(load_content(), 'production')
        report = validate_model(model, 'production')
        self.assertTrue({'restaurant.city', 'restaurant.address', 'restaurant.hours',
                         'restaurant.contacts.whatsappHref', 'restaurant.contacts.emailHref'}
                        <= paths(report.errors))
        message = next(str(i) for i in report.errors if i.path == 'restaurant.contacts.emailHref')
        self.assertEqual(message, 'restaurant.contacts.emailHref: email obrigatório para produção')

    def test_schema_version_and_preview_flag(self):
        self.assertIn('schemaVersion', paths(validate_model(self.model(schemaVersion=2), 'production').errors))
        self.assertIn('schemaVersion', paths(validate_model(self.model(schemaVersion=True), 'production').errors))
        self.assertIn('preview', paths(validate_model(self.model('preview'), 'production').errors))

    def test_unknown_fields_are_rejected(self):
        model = self.model()
        model['restaurant']['whatsappNumber'] = '+351 910 000 000'
        model['debug'] = True
        self.assertTrue({'restaurant.whatsappNumber', '$.debug'} <= paths(validate_model(model, 'production').errors))

    def test_rejects_unsafe_link_schemes(self):
        model = self.model()
        contacts = model['restaurant']['contacts']
        contacts['whatsappHref'] = 'https://evil.example/351910000000'
        contacts['emailHref'] = 'javascript:alert(1)'
        contacts['directionsHref'] = 'http://maps.example.com'
        model['pages']['home']['sections'] = [
            {'id': 's', 'type': 'editorial', 'heading': 'x', 'paragraphs': [], 'imageIds': [],
             'artworkIds': [], 'links': [{'label': 'a', 'href': 'javascript:alert(1)'},
                                         {'label': 'b', 'href': '//evil.example'}]}]
        errors = paths(validate_model(model, 'production').errors)
        self.assertTrue({'restaurant.contacts.whatsappHref', 'restaurant.contacts.emailHref',
                         'restaurant.contacts.directionsHref', 'pages.home.sections[0].links[0].href',
                         'pages.home.sections[0].links[1].href'} <= errors)

    def test_unencoded_whatsapp_message_is_rejected(self):
        model = self.model()
        model['restaurant']['contacts']['whatsappHref'] = 'https://wa.me/351910000000?text=Olá mesa'
        self.assertIn('restaurant.contacts.whatsappHref', paths(validate_model(model, 'production').errors))

    def test_display_and_link_must_match(self):
        model = self.model()
        model['restaurant']['contacts']['phoneHref'] = None
        model['restaurant']['contacts']['emailDisplay'] = 'outro@example.com'
        errors = paths(validate_model(model, 'production').errors)
        self.assertTrue({'restaurant.contacts.phoneHref', 'restaurant.contacts.emailDisplay'} <= errors)

    def test_hours_rules(self):
        model = self.model()
        model['restaurant']['hours'] = [
            {'day': 2, 'closed': False, 'note': None,
             'intervals': [{'opens': '19:00', 'closes': '01:00', 'closesNextDay': False}]},
            {'day': 2, 'closed': True, 'note': None,
             'intervals': [{'opens': '25:00', 'closes': '12:00', 'closesNextDay': False}]},
            {'day': 8, 'closed': False, 'note': None, 'intervals': []},
        ]
        errors = paths(validate_model(model, 'production').errors)
        self.assertTrue({'restaurant.hours[0].intervals[0].closes', 'restaurant.hours[1].day',
                         'restaurant.hours[1].intervals', 'restaurant.hours[1].intervals[0].opens',
                         'restaurant.hours[2].day', 'restaurant.hours[2].intervals'} <= errors)

    def test_pages_and_sections(self):
        model = self.model()
        del model['pages']['privacy']
        model['pages']['blog'] = support.page()
        model['pages']['home']['title'] = None
        model['pages']['home']['heroImageId'] = 'missing'
        model['pages']['house']['sections'] = [
            {'id': 'a', 'type': 'editorial', 'heading': 'x', 'paragraphs': [], 'imageIds': ['nope'],
             'artworkIds': ['ghost'], 'links': []},
            {'id': 'a', 'type': 'carousel', 'heading': 'y', 'paragraphs': [], 'imageIds': [],
             'artworkIds': [], 'links': []},
        ]
        errors = paths(validate_model(model, 'production').errors)
        self.assertTrue({'pages.privacy', 'pages.blog', 'pages.home.title', 'pages.home.heroImageId',
                         'pages.house.sections[0].imageIds[0]', 'pages.house.sections[0].artworkIds[0]',
                         'pages.house.sections[1].id', 'pages.house.sections[1].type'} <= errors)

    def test_images(self):
        model = self.model()
        model['images'] = {
            'a': {'id': 'a', 'src': '/assets/../secret.jpg', 'width': True, 'height': 0, 'alt': None,
                  'caption': None, 'credit': None, 'mobileImageId': 'a', 'focalPoint': {'x': 2, 'y': 0},
                  'variants': [{'src': 'https://cdn.example/a.jpg', 'width': 1, 'height': 1,
                                'mimeType': 'image/gif'}]},
            'b': {'id': 'other', 'src': '/Users/me/photo.jpg', 'width': 1, 'height': 1, 'alt': 'x',
                  'caption': None, 'credit': None, 'variants': [], 'mobileImageId': 'zzz', 'focalPoint': None},
        }
        errors = paths(validate_model(model, 'production').errors)
        self.assertTrue({'images.a.src', 'images.a.width', 'images.a.height', 'images.a.alt',
                         'images.a.mobileImageId', 'images.a.focalPoint.x', 'images.a.variants[0].src',
                         'images.a.variants[0].mimeType', 'images.b.id', 'images.b.src',
                         'images.b.mobileImageId'} <= errors)

    def test_missing_image_file_is_error_only_in_production(self):
        with tempfile.TemporaryDirectory() as tmp:
            for mode in ('preview', 'production'):
                model = self.model(mode)
                model['images'] = {'a': {'id': 'a', 'src': '/assets/photos/a.webp', 'width': 1, 'height': 1,
                                         'alt': 'x', 'caption': None, 'credit': None, 'variants': [],
                                         'mobileImageId': None, 'focalPoint': None}}
                report = validate_model(model, mode, public_dir=tmp)
                bucket = report.errors if mode == 'production' else report.warnings
                self.assertIn('images.a.src', paths(bucket), mode)
            Path(tmp, 'assets/photos').mkdir(parents=True)
            Path(tmp, 'assets/photos/a.webp').write_bytes(b'x')
            self.assertEqual(validate_model(model, 'production', public_dir=tmp).errors, [])

    def test_artworks(self):
        model = self.model()
        model['artworks'] = [
            {'id': 'w', 'artistId': 'x', 'title': '', 'year': None, 'technique': None, 'dimensions': None,
             'description': None, 'imageId': 'none', 'fullImageId': 'none', 'order': '1', 'featured': 1,
             'published': True},
            {'id': 'w', 'artistId': 'x', 'title': 'T', 'year': None, 'technique': None, 'dimensions': None,
             'description': None, 'imageId': 'none', 'fullImageId': 'none', 'order': 1, 'featured': False},
        ]
        errors = paths(validate_model(model, 'production').errors)
        self.assertTrue({'artworks[0].title', 'artworks[0].imageId', 'artworks[0].order',
                         'artworks[0].featured', 'artworks[0].published', 'artworks[1].id',
                         'artist'} <= errors)

    def test_menu_demo_cannot_be_published(self):
        model = self.model(navigation={'menuEnabled': True})
        self.assertIn('navigation.menuEnabled', paths(validate_model(model, 'production').errors))
        preview = self.model('preview', navigation={'menuEnabled': True})
        self.assertIn('navigation.menuEnabled', paths(validate_model(preview, 'preview').warnings))

    def test_malformed_input_does_not_crash(self):
        for broken in (None, [], {'pages': [], 'images': [], 'artworks': {}, 'restaurant': 'x'},
                       {'pages': {'home': {'sections': [{'artworkIds': [[1]], 'type': ['x']}]}}}):
            report = validate_model(broken, 'production')
            self.assertFalse(report.ok)


if __name__ == '__main__':
    unittest.main()

