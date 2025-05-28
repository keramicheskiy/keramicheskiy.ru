from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    ORIENTATIONS = (
        (1, "Straight"),
        (2, "Gay"),
        (3, "Lesbian"),
        (4, "Bisexual"),
        (5, "Other"),
    )
    is_verified = models.BooleanField(default=False)
    is_not_banned = models.BooleanField(default=True)
    sexual_orientation = models.PositiveSmallIntegerField(choices=ORIENTATIONS, null=True, blank=True)


class VerifyCode(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    code = models.CharField(max_length=10)
