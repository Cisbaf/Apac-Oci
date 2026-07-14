#!/usr/bin/env bash
# Gate único de verificação. Roda todos os testes e o lint.
# Falha (exit != 0) se QUALQUER gate falhar. Ver .context/workflow.md.
#
# Pré-requisitos:
#   - venv do backend criada em backend/.venv (python3 -m venv backend/.venv;
#     pip install -r backend/requirements.txt -r backend/core/requirements.txt).
#     Este script ativa a venv sozinho se ela existir.
#   - node_modules do frontend instalado (cd frontend && npm ci).
set -uo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

VENV="$ROOT/backend/.venv"
if [ -f "$VENV/bin/activate" ]; then
  # shellcheck disable=SC1091
  source "$VENV/bin/activate"
else
  echo "⚠️  venv não encontrada em backend/.venv — crie com:"
  echo "    python3 -m venv backend/.venv && source backend/.venv/bin/activate"
  echo "    pip install -r backend/requirements.txt -r backend/core/requirements.txt"
fi

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

# Backend — domínio e use cases (sem banco, pytest puro)
run "backend/core (pytest)" bash -c "cd '$ROOT/backend/core' && python -m pytest -q"
# Backend — integração Django (sem pytest-django configurado: usa o test runner do Django)
run "backend/src (manage.py test)" bash -c "cd '$ROOT/backend/src' && python manage.py test"
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
