#!/usr/bin/env bash
# Gate único de verificação. Roda todos os testes e o lint.
# Falha (exit != 0) se QUALQUER gate falhar. Ver .context/workflow.md.
# T-001 deve ajustar caminhos/ativação de venv conforme o ambiente real.
set -uo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

fail=0
run() {
  local nome="$1"; shift
  echo ""
  echo "▶ $nome"
  if ( "$@" ); then
    echo "✅ $nome"
  else
    echo "❌ $nome"
    fail=1
  fi
}

# Backend — domínio e use cases (sem banco)
run "backend/core (pytest)" bash -c "cd '$ROOT/backend/core' && python -m pytest -q"
# Backend — integração Django
run "backend/src (pytest)"  bash -c "cd '$ROOT/backend/src'  && python -m pytest -q"
# Frontend — testes
run "frontend (jest)"       bash -c "cd '$ROOT/frontend' && npm test --silent"
# Frontend — lint
run "frontend (lint)"       bash -c "cd '$ROOT/frontend' && npm run lint"

echo ""
if [ "$fail" -eq 0 ]; then
  echo "══════════════════════════════"
  echo "✅ TODOS OS GATES PASSARAM"
  echo "══════════════════════════════"
else
  echo "══════════════════════════════"
  echo "❌ HÁ GATES VERMELHOS — não faça merge"
  echo "══════════════════════════════"
fi
exit "$fail"
