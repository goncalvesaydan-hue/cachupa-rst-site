#!/usr/bin/env bash
set -eu
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
command -v python3 >/dev/null || { echo 'Python 3 é necessário para a base atual.'; exit 1; }
command -v node >/dev/null || { echo 'Node é necessário para verificar o JavaScript.'; exit 1; }
command -v npm >/dev/null || { echo 'npm é necessário para os futuros scripts dos módulos.'; exit 1; }
python3 - <<'PY'
import json
from pathlib import Path
for module in ('frontend', 'backend'):
    json.loads(Path(module, 'package.json').read_text())
print('Manifestos válidos. Estrutura preparada; aplicação ainda não migrada.')
PY
echo 'Nada instalado ou publicado. Ler docs/orca-briefing.md antes de implementar.'
