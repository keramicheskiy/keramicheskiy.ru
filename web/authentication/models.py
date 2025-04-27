from django.contrib.auth.models import AbstractUser
from django.db import models



class CustomUser(AbstractUser):
    is_confirmed = models.BooleanField(default=False)
    is_not_banned = models.BooleanField(default=True)






