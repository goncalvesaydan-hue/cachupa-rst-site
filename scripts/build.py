"""Build the public site using the canonical backend validation and frontend renderer."""
import argparse
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BACKEND_SRC = ROOT / 'backend' / 'src'
if str(BACKEND_SRC) not in sys.path:
    sys.path.insert(0, str(BACKEND_SRC))

from data_loader import ContentError, load_content
from generator import PUBLIC_DIR, BuildError, build_site
from normalizer import normalize_content
from validator import validate_model

ROOT_PAGES = (
    'index.html',
    '404.html',
    'a-nossa-casa/index.html',
    'contactos/index.html',
    'galeria/index.html',
    'privacidade/index.html',
    'reservas/index.html',
)


def _sync_root(dist_dir):
    for rel in ROOT_PAGES:
        target = ROOT / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(dist_dir / rel, target)

    for rel in ('assets/site.css', 'assets/site.js'):
        target = ROOT / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(dist_dir / rel, target)

    for folder in ('assets/brand', 'assets/photos'):
        source_root = dist_dir / folder
        if not source_root.is_dir():
            continue
        for src in source_root.rglob('*'):
            if src.is_file():
                dst = ROOT / src.relative_to(dist_dir)
                if not dst.exists() or src.read_bytes() != dst.read_bytes():
                    dst.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copyfile(src, dst)

    (ROOT / '.nojekyll').write_text('', encoding='utf-8')


def main(argv=None):
    parser = argparse.ArgumentParser(description='Gerar a distribuição do site Cachupa Rst.')
    parser.add_argument('--mode', choices=('production', 'preview'), default='production')
    parser.add_argument('--no-sync-root', action='store_true', help='Gerar apenas em backend/dist/')
    args = parser.parse_args(argv)

    try:
        source = load_content()
    except ContentError as exc:
        print(f'erro: {exc}', file=sys.stderr)
        return 2

    model = normalize_content(source, args.mode)
    report = validate_model(model, args.mode, public_dir=PUBLIC_DIR)
    for item in report.warnings:
        print(f'aviso: {item}', file=sys.stderr)
    for item in report.errors:
        print(f'erro: {item}', file=sys.stderr)
    if not report.ok:
        return 1

    dist_dir = ROOT / 'backend' / 'dist' / args.mode
    try:
        files = build_site(model, dist_dir)
    except BuildError as exc:
        print(f'erro: {exc}', file=sys.stderr)
        return 2

    if args.mode == 'production' and not args.no_sync_root:
        _sync_root(dist_dir)

    pages = sum(1 for name in files if name.endswith('.html') and name != 'menu/index.html')
    print(f'{pages} páginas e {len(files) - pages} recursos gerados em {dist_dir}. Menu preservado.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
