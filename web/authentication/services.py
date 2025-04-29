from random import randint

from .models import VerifyCode
from .tasks import send_verification_email


def verify_email(user):
    code = str(randint(0, 9999)).zfill(4)
    send_verification_email.delay(user.email, code)
    (verify_code, created) = VerifyCode.objects.get_or_create(user=user)
    verify_code.code = code
    verify_code.save()
