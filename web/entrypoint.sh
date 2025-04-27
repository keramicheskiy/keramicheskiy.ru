#!/bin/bash

# Выполняем collectstatic
echo "Собираем статические файлы..."
python manage.py collectstatic --noinput

# Копируем новые статические файлы из /web/static в volume static-data
echo "Перезаписываем файлы в volume static-data..."
cp -r /web/static/* /static-data/

# Теперь запускаем основной процесс (например, gunicorn)
exec "$@"
