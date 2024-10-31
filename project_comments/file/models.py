from django.db import models
from comments.models import Comment


class File(models.Model):
    """
    Represents a file associated with a comment.

    Attributes:
        FILE_TYPES (list): A list of tuples representing the allowed file types.
        filetype (CharField): The type of file, either 'image' or 'document'.
        filepath (FileField): The path where the file is stored.
        comment (ForeignKey): The comment associated with this file.
        created_at (DateTimeField): The timestamp when the file was created.
    """
    FILE_TYPES = [
        ('image', 'Image'),
        ('document', 'Document'),
    ]
    filetype = models.CharField(max_length=10, choices=FILE_TYPES)
    filepath = models.FileField(upload_to='uploads/')
    comment = models.ForeignKey(
        Comment,
        on_delete=models.CASCADE,
        related_name="files")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """
        Returns the string representation of the File instance.

        Returns:
            str: The file path of the stored file.
        """
        return self.filepath
