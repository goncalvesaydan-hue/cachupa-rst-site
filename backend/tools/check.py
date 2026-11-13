"""Syntax check for backend Python files and content JSON. Writes nothing."""
import ast
import json
import sys
from pathlib import Path

BACKEND = Path(__file__).resolve().parents[1]
CONTENT = BACKEND.parent / 'content'


def main():
    python_files = sorted(p for folder in ('src', 'tests', 'tools') for p in (BACKEND / folder).glob('*.py'))
    json_files = sorted(CONTENT.glob('*.json'))
    failures = []
    for path in python_files:
        try:
            ast.parse(path.read_text(encoding='utf-8'), filename=str(path))
        except SyntaxError as exc:
            failures.append(f'{path}:{exc.lineno}: {exc.msg}')
    for path in json_files:
        try:
            json.loads(path.read_text(encoding='utf-8'))
        except json.JSONDecodeError as exc:
            failures.append(f'{path}:{exc.lineno}: {exc.msg}')
    for failure in failures:
        print(failure, file=sys.stderr)
    if failures:
        return 1
    print(f'{len(python_files)} ficheiros Python e {len(json_files)} JSON de conteúdo: sintaxe válida.')
    return 0


if __name__ == '__main__':
    sys.exit(main())

