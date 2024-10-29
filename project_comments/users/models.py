from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    create_time = models.DateTimeField(auto_now_add=True)
    home_page = models.URLField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.username
