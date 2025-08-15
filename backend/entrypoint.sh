#!/bin/sh
python src/manage.py migrate --noinput
python src/manage.py collectstatic --noinput
gunicorn src.app.wsgi:application --bind 0.0.0.0:8000
