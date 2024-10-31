from django.shortcuts import render, redirect
from .models import User
from .forms import UserRegistrationForm
from django.contrib.auth.decorators import login_required


@login_required(login_url='login')
def user_list(request):
    """
    View function to list all registered users.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The rendered HTML response containing the list of users.
    """
    users = User.objects.all()
    return render(request, 'users/users_list.html', {'users': users})


def register(request):
    """
    View function for user registration.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The rendered HTML response containing the registration form.
    """
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()  # Сохраняем нового пользователя в базе данных
            # Перенаправляем на страницу входа после регистрации
            return redirect('users_list')
    else:
        form = UserRegistrationForm()
    return render(request, 'registration/register.html',
                  {'form': form})  # Отображаем форму
