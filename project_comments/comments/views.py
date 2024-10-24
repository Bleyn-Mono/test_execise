from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from users.views import register
from .models import Comment
from .forms import CommentForm
from django.contrib.auth.models import User


Useer = get_user_model()

def comment_list(request):
    comments = Comment.objects.filter(parent__isnull=True) #отображаем только родительские коментарии
    return render(request, 'comments/comment_list.html', {'comments': comments})


@login_required(login_url='login')
def comment_create(request, parent_id=None):
    if request.method == 'POST':
        form = CommentForm(request.POST)
        #если запрос POST отправленна форма
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user  # Используем текущего авторизованного пользователя
            # если parent_id передан
            if parent_id:
                parent_comment = get_object_or_404(Comment, id=parent_id)
                comment.parent = parent_comment
            comment.save()  # Сохраняем комментарий в базу данных
            return redirect('comment_list')
    # Если GET-запрос (просто отображение формы)
    else:
        form = CommentForm()
    return render(request, 'comments/creat_comment.html', {'form': form})


@login_required(login_url='login')
def comment_update(request, comment_id):
    comment = Comment.objects.get(id=comment_id)
    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            return redirect('comment_list')
    else:
        form = CommentForm(instance=comment)
    return render(request, 'comments/update_comment.html', {'form': form})


@login_required(login_url='login')
def comment_delete(request, comment_id):
    comment = Comment.objects.get(id=comment_id)
    if request.method == 'POST':
        comment.delete()
        return redirect('comment_list')
    return render(request, 'comments/delete_comment.html', {'comment': comment})
