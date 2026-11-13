import contextlib
import hashlib
import io
import json
import tempfile
import unittest
from pathlib import Path

import support
from generator import MARKER, BuildError, build_site
from main import main
from normalizer import normalize_content

PAGES = {'index.html', 'a-nossa-casa/index.html', 'galeria/index.html', 'reservas/index.html',
         'contactos/index.html', 'privacidade/index.html', '404.html'}


def tree_digest(*folders):
    digest = hashlib.sha256()
    for folder in folders:
        for path in sorted(p for p in folder.rglob('*') if p.is_file() and '__pycache__' not in p.parts):
            digest.update(str(path).encode())
            digest.update(path.read_bytes())
    return digest.hexdigest()


def run(*argv):
    out, err = io.StringIO(), io.StringIO()
    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
        code = main(list(argv))
    return code, out.getvalue(), err.getvalue()


class GeneratorTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.base = Path(self.tmp.name)

    def test_preview_build_renders_all_routes_without_touching_sources(self):
        sources = (support.ROOT / 'content', support.ROOT / 'frontend' / 'src', support.ROOT / 'frontend' / 'public')
        before = tree_digest(*sources)
        out = self.base / 'site'
        files = build_site(normalize_content(support.complete_source(), 'preview'), out)
        self.assertEqual(tree_digest(*sources), before)
        self.assertTrue(PAGES <= set(files))
        self.assertTrue({'assets/site.css', 'assets/site.js', 'assets/brand/logo.svg', 'robots.txt', MARKER} <= set(files))
        home = (out / 'index.html').read_text(encoding='utf-8')
        self.assertIn('noindex', home)
        self.assertIn('https://wa.me/351910000000?text=Ol%C3%A1', home)
        self.assertEqual(json.loads((out / MARKER).read_text())['mode'], 'preview')
        self.assertFalse((out / 'assets' / 'photos').exists())  # nothing referenced, nothing published
        self.assertEqual([p.name for p in self.base.iterdir()], ['site'])  # staging folder cleaned up

    def test_production_build_has_no_preview_markers(self):
        out = self.base / 'prod'
        files = build_site(normalize_content(support.complete_source(), 'production'), out)
        self.assertNotIn('robots.txt', files)
        self.assertNotIn('noindex', (out / 'index.html').read_text(encoding='utf-8'))

    def test_only_referenced_images_are_copied(self):
        public = self.base / 'public'
        (public / 'assets' / 'photos').mkdir(parents=True)
        for name in ('used.webp', 'used-480.webp', 'private.webp'):
            (public / 'assets' / 'photos' / name).write_bytes(name.encode())
        source = support.complete_source()
        source['images'] = {'used': {'id': 'used', 'src': '/assets/photos/used.webp', 'width': 10, 'height': 10,
                                     'alt': 'Prato', 'variants': [{'src': '/assets/photos/used-480.webp',
                                                                   'width': 480, 'height': 480,
                                                                   'mimeType': 'image/webp'}]}}
        source['pages']['home']['heroImageId'] = 'used'
        out = self.base / 'site'
        build_site(normalize_content(source), out, public_dir=public)
        self.assertEqual(sorted(p.name for p in (out / 'assets' / 'photos').iterdir()),
                         ['used-480.webp', 'used.webp'])

    def test_refuses_unsafe_destinations(self):
        model = normalize_content(support.complete_source())
        for target in (support.ROOT, support.ROOT.parent, support.ROOT / 'content' / 'out',
                       support.ROOT / 'frontend' / 'dist', support.ROOT / 'backend' / 'src'):
            with self.subTest(target=target), self.assertRaises(BuildError):
                build_site(model, target)

    def test_never_deletes_foreign_folder_but_replaces_own_build(self):
        model = normalize_content(support.complete_source())
        foreign = self.base / 'foreign'
        foreign.mkdir()
        (foreign / 'keep.txt').write_text('x')
        with self.assertRaisesRegex(BuildError, 'nada foi apagado'):
            build_site(model, foreign)
        self.assertTrue((foreign / 'keep.txt').exists())

        own = self.base / 'own'
        build_site(model, own)
        (own / 'stale.html').write_text('old')
        build_site(model, own)
        self.assertFalse((own / 'stale.html').exists())

    def test_build_is_deterministic(self):
        model = normalize_content(support.complete_source())
        build_site(model, self.base / 'a')
        build_site(model, self.base / 'b')
        files_a = {p.relative_to(self.base / 'a'): p.read_bytes() for p in (self.base / 'a').rglob('*') if p.is_file()}
        files_b = {p.relative_to(self.base / 'b'): p.read_bytes() for p in (self.base / 'b').rglob('*') if p.is_file()}
        self.assertEqual(files_a, files_b)


class CliTests(unittest.TestCase):
    def test_validate_real_content(self):
        code, _, err = run('validate', '--mode', 'preview')
        self.assertEqual(code, 0)
        self.assertIn('0 erro(s), 0 aviso(s)', err)
        code, _, err = run('validate', '--mode', 'production')
        self.assertEqual(code, 0)
        self.assertIn('aviso: site.baseUrl', err)

    def test_model_outputs_contract_json(self):
        code, out, _ = run('model')
        self.assertEqual(code, 0)
        model = json.loads(out)
        self.assertEqual((model['schemaVersion'], model['preview']), (1, True))

    def test_unreadable_content_exits_2(self):
        with tempfile.TemporaryDirectory() as tmp:
            Path(tmp, 'site.json').write_text('{', encoding='utf-8')
            self.assertEqual(run('validate', '--content', tmp)[0], 2)

    def test_production_build_of_incomplete_content_writes_nothing(self):
        with tempfile.TemporaryDirectory() as tmp:
            content_dir = Path(tmp) / 'content'
            content_dir.mkdir()
            source = support.complete_source()
            pages = source.pop('pages')
            source['restaurant'] = {'city': None, 'address': None, 'hours': [], 'contacts': {}}
            (content_dir / 'site.json').write_text(json.dumps(source), encoding='utf-8')
            (content_dir / 'pages.json').write_text(json.dumps(pages), encoding='utf-8')
            out = Path(tmp) / 'prod'
            self.assertEqual(run('build', '--mode', 'production', '--content', str(content_dir), '--out', str(out))[0], 1)
            self.assertFalse(out.exists())

    def test_preview_build_of_real_content(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / 'preview'
            code, out_text, _ = run('build', '--out', str(out))
            self.assertEqual(code, 0)
            self.assertIn('7 páginas', out_text)
            self.assertTrue(all((out / name).is_file() for name in PAGES))
            for name in ('menu/index.html', 'menu/style.css', 'menu/data.js', 'menu/script.js', 'menu/brand/logo.svg'):
                self.assertTrue((out / name).is_file(), name)
            self.assertFalse((out / 'menu/README.md').exists())
            self.assertFalse((out / 'menu/tests').exists())


if __name__ == '__main__':
    unittest.main()
