#!/bin/bash

# Собираем статику при запуске контейнера
python manage.py collectstatic --noinput

# Потом запускаем Gunicorn
gunicorn web.wsgi:application --bind 0.0.0.0:8000
