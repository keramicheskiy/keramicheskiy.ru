FROM python:3.9

WORKDIR /web

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Копируем entrypoint.sh в контейнер
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Указываем entrypoint для контейнера
ENTRYPOINT ["/entrypoint.sh"]

# Приложение запускается через gunicorn
CMD ["gunicorn", "web.wsgi:application", "--bind", "0.0.0.0:8000"]


