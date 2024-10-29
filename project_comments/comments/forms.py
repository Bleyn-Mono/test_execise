from django import forms
from .models import Comment
from captcha.fields import CaptchaField
import bleach


class CommentForm(forms.ModelForm):
    user_name = forms.CharField(max_length=150, required=True)  # Имя пользователя
    email = forms.EmailField(required=True)  # E-mail
    home_page = forms.URLField(required=False)  # Домашняя страница
    text = forms.CharField(widget=forms.Textarea, required=True)  # Текст комментария
    captcha = CaptchaField()
    files = forms.FileField(widget=forms.ClearableFileInput(attrs={'allow_multiple_selected': True}), required=False)

    class Meta:
        model = Comment
        fields = ['user_name', 'email', 'home_page', 'text', 'captcha', 'files']

    def clean_text(self):
        text = self.cleaned_data['text']
        allowed_tags = ['a', 'code', 'i', 'strong']
        allowed_attributes = {
            'a': ['href', 'title']
        }

        # Используем bleach.clean для очистки текста и сохраняем очищенный результат
        cleaned_text = bleach.clean(text, tags=allowed_tags, attributes=allowed_attributes)

        # Применяем linkify, чтобы сделать URL кликабельными
        cleaned_text = bleach.linkify(cleaned_text)

        # Проверка, совпадает ли очищенный текст с оригиналом
        if cleaned_text != text:
            raise forms.ValidationError("Некоторые HTML-теги недопустимы или не закрыты.")

        return cleaned_text