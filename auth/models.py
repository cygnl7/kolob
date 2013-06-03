from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager

from ordinances.models import Ward


class WardUser(AbstractUser):
    ward = models.ForeignKey(Ward, null=True)
    objects = UserManager()
