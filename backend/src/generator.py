"""Static generation: validated model + frontend renderer -> explicit output folder.

Presentation stays in frontend/ (render_site, templates, CSS, JS, public assets);
this module only orchestrates. Writes happen exclusively inside the requested
output folder, built in a staging folder and swapped in at the end so a failed
build never leaves a half-written site.
"""
import json
import shutil
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
FRONTEND = ROOT / 'frontend'
PUBLIC_DIR = FRONTEND / 'public'
STATIC_SOURCES = {
    'assets/site.css': FRONTEND / 'src' / 'styles' / 'site.css',
    'assets/site.js': FRONTEND / 'src' / 'scripts' / 'site.js',
}
# Inside the project, builds may only go here (other folders are sources or
# belong to other agents, e.g. frontend/dist).
PROJECT_OUTPUT_ROOT = ROOT / 'backend' / 'dist'
# Photo folders are not copied wholesale: only images referenced by the model are
# published, so unselected or draft-only photos stay private.
IMAGE_DIRS = ('assets/photos', 'assets/images')
MENU_DIR = ROOT / 'menu'
MENU_FILES = ('index.html', 'style.css', 'data.js', 'script.js')
MENU_DIRS = ('brand',)
MARKER = '.cachupa-build'


class BuildError(Exception):
    """The build was refused or could not be completed."""


def _render_site():
    source = str(FRONTEND / 'src')
    if source not in sys.path:
        sys.path.insert(0, source)
    from render import render_site  # frontend-owned presentation adapter
    return render_site


def resolve_output(out_dir):
    """Return the absolute output folder or raise BuildError if it is unsafe."""
    out = Path(out_dir).expanduser().resolve()
    if out == ROOT or out in ROOT.parents:
        raise BuildError(f'destino recusado: {out} é a raiz do projeto ou contém-na')
    if out.is_relative_to(ROOT) and not out.is_relative_to(PROJECT_OUTPUT_ROOT):
        raise BuildError(f'destino recusado: dentro do projeto, a saída do backend tem de ficar em '
                         f'{PROJECT_OUTPUT_ROOT.relative_to(ROOT)}/')
    if out.exists():
        if not out.is_dir():
            raise BuildError(f'destino recusado: {out} existe e não é uma pasta')
        if any(out.iterdir()) and not (out / MARKER).is_file():
            raise BuildError(f'destino recusado: {out} não está vazio e não foi criado por este gerador; '
                             'nada foi apagado')
    return out


def _image_paths(model):
    paths = set()
    for image in model['images'].values():
        paths.add(image['src'])
        paths.update(variant['src'] for variant in image.get('variants', []))
    return sorted(paths)


def _inside(base, relative):
    target = (base / relative).resolve()
    if not target.is_relative_to(base.resolve()):
        raise BuildError(f'caminho de saída inválido: {relative}')
    return target


def _write(staging, model, pages, public_dir):
    public = Path(public_dir).resolve()

    def ignore(directory, names):
        relative = Path(directory).resolve().relative_to(public).as_posix()
        skipped = []
        for name in names:
            path = name if relative == '.' else f'{relative}/{name}'
            if name == '.DS_Store' or name == '.gitkeep' or path in IMAGE_DIRS:
                skipped.append(name)
        return skipped

    shutil.copytree(public, staging, ignore=ignore, dirs_exist_ok=True)

    for src in _image_paths(model):
        source = public / src.lstrip('/')
        if source.is_file():  # missing files are reported by the validator
            target = _inside(staging, src.lstrip('/'))
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source, target)

    for relative, source in STATIC_SOURCES.items():
        target = _inside(staging, relative)
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, target)

    for name in sorted(pages):
        target = _inside(staging, name)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(pages[name], encoding='utf-8')

    if model.get('navigation', {}).get('menuEnabled') and MENU_DIR.is_dir():
        menu_target = _inside(staging, 'menu')
        menu_target.mkdir(parents=True, exist_ok=True)
        for name in MENU_FILES:
            source = MENU_DIR / name
            if source.is_file():
                shutil.copyfile(source, _inside(menu_target, name))
        for dirname in MENU_DIRS:
            source_dir = MENU_DIR / dirname
            if source_dir.is_dir():
                shutil.copytree(
                    source_dir,
                    _inside(menu_target, dirname),
                    ignore=lambda _, names: [n for n in names if n in ('.DS_Store', '.gitkeep')],
                    dirs_exist_ok=True,
                )

    if model['preview']:
        # Pages already carry noindex; robots.txt covers crawlers that skip HTML.
        (staging / 'robots.txt').write_text('User-agent: *\nDisallow: /\n', encoding='utf-8')

    marker = {'generator': 'cachupa-backend', 'schemaVersion': model['schemaVersion'],
              'mode': 'preview' if model['preview'] else 'production'}
    (staging / MARKER).write_text(json.dumps(marker, indent=2) + '\n', encoding='utf-8')


def build_site(model, out_dir, *, public_dir=PUBLIC_DIR):
    """Render `model` (already normalized and validated) into `out_dir`.

    Returns the sorted list of generated files, relative to `out_dir`.
    """
    out = resolve_output(out_dir)
    pages = _render_site()(model)  # render before touching the disk
    out.parent.mkdir(parents=True, exist_ok=True)
    staging = Path(tempfile.mkdtemp(prefix=f'.{out.name}-staging-', dir=out.parent))
    try:
        _write(staging, model, pages, public_dir)
        files = sorted(p.relative_to(staging).as_posix() for p in staging.rglob('*') if p.is_file())
        if out.exists():
            shutil.rmtree(out)
        staging.replace(out)
    except BaseException:
        shutil.rmtree(staging, ignore_errors=True)
        raise
    return files

