#!/bin/bash


python manage.py collectstatic --noinput

# Копирование новых статические файлы из /web/static в volume static-data
cp -r /web/static/* /static-data/

exec gunicorn web.wsgi:application --bind 0.0.0.0:8000
