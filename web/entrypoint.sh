#!/bin/bash


python manage.py collectstatic --noinput

# Копируем новые статические файлы из /web/static в volume static-data
cp -r /web/static/* /static-data/

# Теперь запускаем основной процесс (например, gunicorn)
exec "$@"
