"""Read the editorial sources in content/. Read-only: never writes or repairs files."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CONTENT_DIR = ROOT / 'content'


class ContentError(Exception):
    """A source file is missing or is not valid JSON."""


def _read_json(path):
    try:
        return json.loads(path.read_text(encoding='utf-8'))
    except FileNotFoundError:
        raise ContentError(f'ficheiro de conteúdo em falta: {path}') from None
    except json.JSONDecodeError as exc:
        raise ContentError(
            f'JSON inválido em {path} (linha {exc.lineno}, coluna {exc.colno}): {exc.msg}'
        ) from None


def load_content(content_dir=None):
    """Return the raw editorial source.

    `site.json` holds the restaurant/artist data (legacy format, still read by
    scripts/build.py). `pages.json`, when present, holds the editorial pages keyed
    by contract page key. Keeping pages in a separate file avoids changing the
    structure the legacy generator depends on.
    """
    directory = Path(content_dir) if content_dir else CONTENT_DIR
    data = _read_json(directory / 'site.json')
    if not isinstance(data, dict):
        raise ContentError(f'{directory / "site.json"} deve conter um objeto JSON')

    pages_path = directory / 'pages.json'
    if pages_path.exists():
        pages = _read_json(pages_path)
        if not isinstance(pages, dict):
            raise ContentError(f'{pages_path} deve conter um objeto JSON')
        if 'pages' in data:
            raise ContentError('páginas definidas em site.json e em pages.json; manter uma única fonte')
        data['pages'] = pages
    return data