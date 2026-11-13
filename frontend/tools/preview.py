"""Build an isolated frontend preview, never a production deployment."""
import argparse
import functools
import json
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import shutil
import sys

ROOT = Path(__file__).resolve().parents[1]
MENU_FILES = ('index.html', 'style.css', 'data.js', 'script.js')
MENU_DIRECTORIES = ('brand',)
sys.path.insert(0, str(ROOT / 'src'))
from render import render_site


def copy_menu(source, output):
    """Copy only browser-facing menu files into the preview distribution."""
    source = Path(source)
    target = Path(output) / 'menu'
    target.mkdir(parents=True, exist_ok=True)
    for name in ('assets', 'assets_2'):
        stale_media = target / name
        if stale_media.is_dir():
            shutil.rmtree(stale_media)
        elif stale_media.exists():
            stale_media.unlink()
    for name in MENU_FILES:
        shutil.copyfile(source / name, target / name)
    for name in MENU_DIRECTORIES:
        shutil.copytree(source / name, target / name, dirs_exist_ok=True)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--model', type=Path, default=ROOT / 'fixtures/preview.json')
    parser.add_argument('--serve', action='store_true')
    parser.add_argument('--port', type=int, default=18952)
    args = parser.parse_args()
    model = json.loads(args.model.read_text())
    if model.get('preview') is not True:
        parser.error('Este comando aceita apenas modelos com preview=true.')
    pages = render_site(model)
    output = ROOT / 'dist'
    output.mkdir(exist_ok=True)
    shutil.copytree(ROOT / 'public', output, dirs_exist_ok=True)
    for source in ('styles/site.css', 'scripts/site.js'):
        shutil.copyfile(ROOT / 'src' / source, output / 'assets' / Path(source).name)
    for name, html in pages.items():
        target = output / name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(html, encoding='utf-8')
    if model['navigation']['menuEnabled']:
        copy_menu(ROOT.parent / 'menu', output)
    print(f'{len(pages)} páginas geradas em {output}', flush=True)
    if args.serve:
        class Handler(SimpleHTTPRequestHandler):
            def end_headers(self):
                self.send_header('Cache-Control', 'no-store, must-revalidate')
                super().end_headers()

            def send_error(self, code, message=None, explain=None):
                if code == 404:
                    payload = (output / '404.html').read_bytes()
                    self.send_response(404)
                    self.send_header('Content-Type', 'text/html; charset=utf-8')
                    self.send_header('Content-Length', str(len(payload)))
                    self.end_headers()
                    if self.command != 'HEAD':
                        self.wfile.write(payload)
                else:
                    super().send_error(code, message, explain)
        server = ThreadingHTTPServer(('127.0.0.1', args.port), functools.partial(Handler, directory=str(output)))
        print(f'Preview: http://127.0.0.1:{args.port}', flush=True)
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            server.server_close()

if __name__ == '__main__':
    main()
