#!/usr/bin/env bash
# Sobe o ambiente de DESENVOLVIMENTO: SQLite, hot-reload (bind mounts),
# runserver do Django e `next dev`, DEBUG=True.
set -euo pipefail
cd "$(dirname "$0")"

if [ ! -f .env ]; then
    echo "Nenhum .env encontrado. Criando .env de desenvolvimento a partir de .env.example..."
    cp .env.example .env
    if command -v openssl >/dev/null 2>&1; then
        secret=$(openssl rand -base64 32)
        sed -i.bak "s#^NEXTAUTH_SECRET=.*#NEXTAUTH_SECRET=${secret}#" .env
        rm -f .env.bak
    fi
fi

echo "Subindo ambiente de desenvolvimento..."
docker compose -f docker-compose.yml -f docker-compose.dev.yml up --build
