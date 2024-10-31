from django import forms
from .models import Comment
from captcha.fields import CaptchaField
import bleach
import re


class CommentForm(forms.ModelForm):
    """
    Form for creating and validating a user comment.

    Attributes:
        user_name: CharField for the user's name, required.
        email: EmailField for the user's email address, required.
        home_page: URLField for an optional user homepage.
        text: CharField for the comment text, required.
        captcha: CaptchaField for spam prevention.
        files: FileField to allow optional file attachments.

    Meta:
        model: Associated model is Comment.
        fields: ['user_name', 'email', 'home_page', 'text', 'captcha', 'files']
    """
    user_name = forms.CharField(
        max_length=150,
        required=True)  # Имя пользователя
    email = forms.EmailField(required=True)  # E-mail
    home_page = forms.URLField(required=False)  # Домашняя страница
    text = forms.CharField(
        widget=forms.Textarea,
        required=True)  # Текст комментария
    captcha = CaptchaField()
    files = forms.FileField(
        widget=forms.ClearableFileInput(
            attrs={
                'allow_multiple_selected': True}),
        required=False)

    class Meta:
        model = Comment
        fields = [
            'user_name',
            'email',
            'home_page',
            'text',
            'captcha',
            'files']
    # Серверная валидация

    def clean_email(self):
        """
        Validate that the email is in the correct format.

        Returns:
            The cleaned email data if valid.

        Raises:
            ValidationError: If the email format is invalid.
        """
        email = self.cleaned_data.get('email')
        if not email or not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            raise forms.ValidationError("Invalid email format.")
        return email

    def clean_text(self):
        """
        Cleans and sanitizes the comment text.

        Allows only certain HTML tags and attributes, making URLs clickable.

        Returns:
            Cleaned text with allowed HTML tags and clickable URLs.

        Raises:
            ValidationError: If HTML tags are invalid or improperly closed.
        """
        text = self.cleaned_data['text']
        allowed_tags = ['a', 'code', 'i', 'strong']
        allowed_attributes = {
            'a': ['href', 'title']
        }
        # Используем bleach.clean для очистки текста и сохраняем очищенный
        # результат
        cleaned_text = bleach.clean(
            text, tags=allowed_tags, attributes=allowed_attributes)
        # Применяем linkify, чтобы сделать URL кликабельными
        cleaned_text = bleach.linkify(cleaned_text)
        # Проверка, совпадает ли очищенный текст с оригиналом
        if cleaned_text != text:
            raise forms.ValidationError(
                "Некоторые HTML-теги недопустимы или не закрыты.")
        return cleaned_text
