#!/usr/bin/env bash
set -u
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
failed=0
pending=0
for module in frontend backend; do
  if node -e 'const p=require(process.argv[1]);process.exit(p.scripts?.test?0:1)' "$ROOT/$module/package.json"; then
    npm --prefix "$ROOT/$module" run test || failed=1
  else
    echo "$module: suite ainda não implementada."
    pending=1
  fi
done
if [ "$failed" -ne 0 ]; then exit 1; fi
if [ "$pending" -ne 0 ]; then echo 'Verificação incompleta; não equivale a aprovação de integração.'; exit 2; fi
