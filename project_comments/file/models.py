import datetime

from django.db import models
from comments.models import Comment


class File(models.Model):
    FILE_TYPES = [
        ('image', 'Image'),
        ('video', 'Video'),
        ('document', 'Document'),
    ]
    filetype = models.CharField(max_length=10, choices=FILE_TYPES)
    filepath = models.CharField(max_length=255)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.filepath
