from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)  # Добавляем поле email

    class Meta:
        model = User
        fields = ['username', 'email', 'home_page', 'password1', 'password2']  # Поля формы
