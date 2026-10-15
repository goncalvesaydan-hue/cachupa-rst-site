#!/usr/bin/env bash
set -u
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
failed=0
pending=0
if [ -f assets/site.js ]; then node --check assets/site.js || failed=1; fi
if [ -f scripts/build.py ]; then
  python3 - <<'PY' || failed=1
import ast
from pathlib import Path
ast.parse(Path('scripts/build.py').read_text())
print('Sintaxe do gerador legado: OK')
PY
fi
for module in frontend backend; do
  if node -e 'const p=require(process.argv[1]);process.exit(p.scripts?.lint?0:1)' "$ROOT/$module/package.json"; then
    npm --prefix "$ROOT/$module" run lint || failed=1
  else
    echo "$module: lint do módulo ainda não configurado."
    pending=1
  fi
done
if [ "$failed" -ne 0 ]; then exit 1; fi
if [ "$pending" -ne 0 ]; then echo 'Sintaxe legada verificada; lint modular pendente.'; exit 2; fi
