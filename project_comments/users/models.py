from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    Custom user model extending AbstractUser to include additional fields.

    Attributes:
        create_time (DateTimeField): The timestamp when the user account was created.
        home_page (URLField): The user's homepage URL.
    """
    create_time = models.DateTimeField(auto_now_add=True)
    home_page = models.URLField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.username
