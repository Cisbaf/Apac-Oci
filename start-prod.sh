#!/usr/bin/env bash
# Sobe o ambiente de PRODUÇÃO: MySQL, gunicorn, build otimizado do Next.js,
# DEBUG=False. Exige um .env completo (veja .env.example).
set -euo pipefail
cd "$(dirname "$0")"

if [ ! -f .env ]; then
    echo "Erro: arquivo .env não encontrado." >&2
    echo "Copie .env.example para .env e preencha os valores de produção." >&2
    exit 1
fi

set -a
# shellcheck disable=SC1091
source .env
set +a

required_vars=(DJANGO_SECRET_KEY NEXTAUTH_SECRET MYSQL_DATABASE MYSQL_USER MYSQL_PASSWORD MYSQL_HOST)
missing=()
for var in "${required_vars[@]}"; do
    if [ -z "${!var:-}" ]; then
        missing+=("$var")
    fi
done

if [ ${#missing[@]} -gt 0 ]; then
    echo "Erro: as seguintes variáveis precisam estar definidas em .env para produção: ${missing[*]}" >&2
    exit 1
fi

echo "Subindo ambiente de produção..."
docker compose -f docker-compose.yml build --pull
docker compose -f docker-compose.yml up -d --force-recreate
