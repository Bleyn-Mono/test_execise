from django.shortcuts import render, redirect
from .models import User
from .forms import UserRegistrationForm
from django.contrib.auth.decorators import login_required


@login_required(login_url='login')
def user_list(request):
    users = User.objects.all()
    return render(request, 'users/users_list.html', {'users': users})


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()  # Сохраняем нового пользователя в базе данных
            return redirect('users_list')  # Перенаправляем на страницу входа после регистрации
    else:
        form = UserRegistrationForm()
    return render(request, 'registration/register.html', {'form': form})  # Отображаем форму