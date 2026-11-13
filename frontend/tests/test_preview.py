import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
from preview import copy_menu


class PreviewMenuCopyTests(unittest.TestCase):
    def test_copies_public_files_and_excludes_project_material(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            source = root / 'source'
            output = root / 'output'
            for name in ('assets', 'assets_2'):
                stale_media = output / 'menu' / name
                stale_media.mkdir(parents=True)
                (stale_media / 'old-menu-photo.jpg').write_text('stale preview file', encoding='utf-8')
            for name in ('index.html', 'style.css', 'data.js', 'script.js'):
                (source / name).parent.mkdir(parents=True, exist_ok=True)
                (source / name).write_text(name, encoding='utf-8')
            for name in ('brand',):
                directory = source / name
                directory.mkdir(parents=True, exist_ok=True)
                (directory / 'public-file').write_text(name, encoding='utf-8')
            for name in ('assets', 'assets_2'):
                directory = source / name
                directory.mkdir(parents=True, exist_ok=True)
                (directory / 'old-menu-photo.jpg').write_text('not part of approved catalog', encoding='utf-8')
            (source / 'README.md').write_text('private project notes', encoding='utf-8')
            (source / 'tests').mkdir()
            (source / 'tests' / 'menu.test.cjs').write_text('test', encoding='utf-8')

            copy_menu(source, output)

            copied = output / 'menu'
            for name in ('index.html', 'style.css', 'data.js', 'script.js', 'brand/public-file'):
                self.assertTrue((copied / name).is_file(), name)
            self.assertFalse((copied / 'assets').exists())
            self.assertFalse((copied / 'assets_2').exists())
            self.assertFalse((copied / 'README.md').exists())
            self.assertFalse((copied / 'tests').exists())


if __name__ == '__main__':
    unittest.main()
