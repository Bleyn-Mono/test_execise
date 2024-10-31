from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User


class UserRegistrationForm(UserCreationForm):
    """
    A form for user registration, extending the built-in UserCreationForm.

    Attributes:
        email (EmailField): The email field for the user registration.

    Meta:
        model (User): The User model associated with this form.
        fields (list): The fields included in the registration form.
    """
    email = forms.EmailField(required=True)  # Добавляем поле email

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'home_page',
            'password1',
            'password2']  # Поля формы
