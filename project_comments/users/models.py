from django.db import models


class User(models.Model):
    username = models.CharField(max_length=50)
    email = models.EmailField(max_length=255)
    create_time = models.DateTimeField(auto_now_add=True)
    home_page = models.URLField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.username
