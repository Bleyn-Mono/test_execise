from django.db import models
from users.models import User
import bleach


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, related_name='children')
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    #переопределяем метод
    def save(self, *args, **kwargs):
        # Очищаем текст комментария перед сохранением
        allowed_tags = ['a', 'code', 'i', 'strong']
        allowed_attributes = {
            'a': ['href', 'title']
        }
        self.text = bleach.clean(self.text, tags=allowed_tags, attributes=allowed_attributes)
        super().save(*args, **kwargs)
