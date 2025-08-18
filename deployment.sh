git pull
docker compose build --pull --no-cache   # opcional, só se quiser garantir rebuild
docker compose up -d --force-recreate
