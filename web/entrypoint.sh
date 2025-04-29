#!/bin/bash

# Статика
python manage.py collectstatic --noinput
cp -r /web/static/* /static-data/ || echo "Static files copy skipped"

exec "$@"

## Запуск Celery в фоне
#celery -A web worker --loglevel=info &
#
## Запуск Gunicorn (основной процесс)
#exec gunicorn web.wsgi:application --bind 0.0.0.0:8000