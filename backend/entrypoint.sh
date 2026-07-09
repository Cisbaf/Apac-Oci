#!/bin/sh
set -e

python manage.py migrate --noinput

if [ "$DJANGO_ENV" = "development" ]; then
    exec python manage.py runserver 0.0.0.0:8000
else
    python manage.py collectstatic --noinput
    exec gunicorn app.wsgi:application --bind 0.0.0.0:8000 --workers 3 --threads 2
fi
