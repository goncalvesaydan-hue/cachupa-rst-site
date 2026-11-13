"""Command line for the Cachupa Rst backend.

    python3 backend/src/main.py validate [--mode preview|production] [--content DIR]
    python3 backend/src/main.py model    [--mode preview|production] [--content DIR]
    python3 backend/src/main.py build --out DIR [--mode preview|production] [--content DIR]

Pipeline: load content/ -> normalize -> validate -> (print model | generate site).
Exit codes: 0 success, 1 validation or generation failure, 2 unreadable content or
refused output folder.
"""
import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from data_loader import ContentError, load_content
from generator import PUBLIC_DIR, BuildError, build_site
from normalizer import normalize_content
from validator import validate_model


def prepare(mode, content_dir=None, public_dir=PUBLIC_DIR):
    """Return (model, report). Normalization happens before validation: the
    source is in the editorial format, the contract applies to the public model."""
    model = normalize_content(load_content(content_dir), mode)
    return model, validate_model(model, mode, public_dir=public_dir)


def _print_report(report, mode):
    for issue in report.warnings:
        print(f'aviso: {issue}', file=sys.stderr)
    for issue in report.errors:
        print(f'erro: {issue}', file=sys.stderr)
    label = 'pré-visualização' if mode == 'preview' else 'produção'
    print(f'{label}: {len(report.errors)} erro(s), {len(report.warnings)} aviso(s)', file=sys.stderr)


def _parser():
    parser = argparse.ArgumentParser(prog='cachupa-backend',
                                     description='Validação, normalização e geração do site Cachupa Rst.')
    commands = parser.add_subparsers(dest='command', required=True)
    for name, text in (('validate', 'validar o conteúdo'),
                       ('model', 'imprimir o modelo público v1 em JSON'),
                       ('build', 'gerar o site estático numa pasta explícita')):
        command = commands.add_parser(name, help=text)
        command.add_argument('--mode', choices=('preview', 'production'), default='preview')
        command.add_argument('--content', type=Path, help='pasta de conteúdo (por omissão: content/)')
        if name == 'build':
            command.add_argument('--out', type=Path, required=True, help='pasta de saída')
    return parser


def main(argv=None):
    args = _parser().parse_args(argv)
    try:
        model, report = prepare(args.mode, args.content)
    except ContentError as exc:
        print(f'erro: {exc}', file=sys.stderr)
        return 2
    _print_report(report, args.mode)
    if not report.ok:
        return 1

    if args.command == 'model':
        json.dump(model, sys.stdout, ensure_ascii=False, indent=2)
        print()
    elif args.command == 'build':
        try:
            files = build_site(model, args.out)
        except BuildError as exc:
            print(f'erro: {exc}', file=sys.stderr)
            return 2
        except (KeyError, TypeError, ValueError) as exc:
            print(f'erro na geração: {exc!r}', file=sys.stderr)
            return 1
        pages = sum(1 for name in files if name.endswith('.html') and name != 'menu/index.html')
        print(f'{pages} páginas e {len(files) - pages} recursos gerados em {Path(args.out).resolve()}')
    return 0


if __name__ == '__main__':
    sys.exit(main())