from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from users.views import register
from .models import Comment
from .forms import CommentForm
from django.urls import reverse
from file.models import File
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.template.loader import render_to_string


Useer = get_user_model()


def get_sorted_comments(request):
    '''function to sort comment by field'''
    sort_by = request.GET.get('sort_by', 'created_at') #по умолчанию сортировка по дате
    order = request.GET.get('order', 'desc')  # Направление по умолчанию - по убыванию
    allowed_sort_fields = {
        'username': 'user__username',
        'email': 'user__email',
        'created_at': 'created_at'
    }
    # Выбираем поле для сортировки и направление
    sort_field = allowed_sort_fields.get(sort_by, 'created_at')
    if order == 'desc':
        sort_field = f'-{sort_field}'
    # Фильтруем только заглавные комментарии (те, у которых parent = None)
    comments = Comment.objects.filter(parent__isnull=True)
    # Проверяем, разрешено ли поле для сортировки
    comments = comments.order_by(sort_field)
    return comments


def comment_list(request):
    # Проверка наличия параметров `sort_by` и `order`
    if 'sort_by' not in request.GET and 'order' not in request.GET:
        base_url = reverse('comment_list')
        query_string = '?sort_by=created_at&order=desc'
        return redirect(base_url + query_string)
    comments = get_sorted_comments(request)
    #пагинатор
    comments_paginator = Paginator(comments, 25)
    paginator_number = request.GET.get('page')
    try:
        comments_page = comments_paginator.page(paginator_number)
    except PageNotAnInteger:
        # Если номер страницы не является целым числом, показываем первую страницу
        comments_page = comments_paginator.page(1)
    except EmptyPage:
        # Если номер страницы выходит за пределы, показываем последнюю страницу
        comments_page = comments_paginator.page(comments_paginator.num_pages)
    return render(request, 'comments/comment_list.html', {'comments': comments_page})


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
            # Обработка загруженных файлов
            for file in request.FILES.getlist('files'):
                file_type = 'image' if file.content_type.startswith('image') else 'document'
                File.objects.create(filetype=file_type, filepath=file, comment=comment)
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

def preview_comment(request):  #проверяем валидацию на стороне сервера
    if request.method == "POST":
        text = request.POST.get("text", "")
        user = request.user
        context = {
            "text": text,
            "user": user,
        }
        preview_html = render_to_string("comments/preview_comment.html", context)
        return JsonResponse({"preview": preview_html})
    return JsonResponse({"error": "Invalid request"}, status=400)