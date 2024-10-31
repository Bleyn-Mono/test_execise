from django.db import models
from users.models import User
import bleach


class Comment(models.Model):
    """
    Model representing a user comment with hierarchical structure and text sanitization.

    Attributes:
        user: ForeignKey linking the comment to the User model.
        parent: ForeignKey for establishing parent-child comment relationships.
        text: TextField containing the content of the comment.
        created_at: DateTimeField recording when the comment was created.
        updated_at: DateTimeField recording the last update time of the comment.
    """

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name='children')
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # переопределяем метод
    def save(self, *args, **kwargs):
        """
        Save method overridden to sanitize the text content of the comment before saving.

        Cleans the comment text using allowed HTML tags and attributes to prevent XSS attacks.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.
        """
        # Очищаем текст комментария перед сохранением
        allowed_tags = ['a', 'code', 'i', 'strong']
        allowed_attributes = {
            'a': ['href', 'title']
        }
        self.text = bleach.clean(
            self.text,
            tags=allowed_tags,
            attributes=allowed_attributes)
        super().save(*args, **kwargs)
