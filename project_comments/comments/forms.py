from django import forms
from .models import Comment



class CommentForm(forms.ModelForm):
    user_name = forms.CharField(max_length=150, required=True)  # Имя пользователя
    email = forms.EmailField(required=True)  # E-mail
    home_page = forms.URLField(required=False)  # Домашняя страница
    text = forms.CharField(widget=forms.Textarea, required=True)  # Текст комментария
    class Meta:
        model = Comment
        fields = ['user_name', 'email', 'home_page', 'text']
