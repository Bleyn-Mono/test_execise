import datetime

from django.db import models
from comments.models import Comment


class File(models.Model):
    FILE_TYPES = [
        ('image', 'Image'),
        ('document', 'Document'),
    ]
    filetype = models.CharField(max_length=10, choices=FILE_TYPES)
    filepath = models.FileField(upload_to='uploads/')
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name="files")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.filepath
