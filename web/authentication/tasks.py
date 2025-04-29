import smtplib
from datetime import time
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from time import sleep

from celery import shared_task

from web.settings import sender_email, email_password, smtp_server, smtp_port


@shared_task
def send_verification_email(receiver_email, code):
    text = (f"Для подтверждения регистрации введите в настройках аккаунта код: {code}.\n "
            f"Если вы не делали запрос на регистрацию, проигнорируйте данное письмо.")

    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = "Подтверждение регистрации"

    message.attach(MIMEText(text, "plain"))

    try:
        server = smtplib.SMTP_SSL(smtp_server, smtp_port)  # SSL-соединение
        server.login(sender_email, email_password)
        server.sendmail(sender_email, receiver_email, message.as_string())
        print("Письмо успешно отправлено!")
        return True
    except Exception as e:
        print(f"Ошибка отправки: {e}")
        return False

#
# import logging
#
# logger = logging.getLogger(__name__)
#
# @shared_task(bind=True)
# def my_task(self, arg1, arg2):
#     try:
#         # Код задачи
#         return "Success"
#     except Exception as e:
#         self.retry(exc=e)