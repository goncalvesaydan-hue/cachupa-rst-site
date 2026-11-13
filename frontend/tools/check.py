"""Dependency-free source checks. Not a substitute for browser testing."""
import ast
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
for folder in ('src', 'tools', 'tests'):
    for path in (ROOT / folder).rglob('*.py'):
        ast.parse(path.read_text(), filename=str(path))
json.loads((ROOT / 'fixtures/preview.json').read_text())
subprocess.run(['node', '--check', str(ROOT / 'src/scripts/site.js')], check=True)
print('Python, JSON e JavaScript: sintaxe válida.')
