from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from .models import Comment
from .forms import CommentForm
from django.urls import reverse
from file.models import File
from django.http import JsonResponse
from django.template.loader import render_to_string


Useer = get_user_model()


def get_sorted_comments(request):
    """
    Sorts comments based on a specified field and order.

    Args:
        request: The HTTP request object, containing GET parameters
                 for `sort_by` (field to sort by) and `order` (sorting direction).

    Returns:
        QuerySet of sorted Comment objects, filtered to include only top-level comments.
    """
    sort_by = request.GET.get(
        'sort_by', 'created_at')  # по умолчанию сортировка по дате
    # Направление по умолчанию - по убыванию
    order = request.GET.get('order', 'desc')
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
    """
    Renders a paginated list of comments with optional sorting.

    If `sort_by` and `order` parameters are not present, defaults to sorting
    by `created_at` in descending order.

    Args:
        request: The HTTP request object.

    Returns:
        HTTPResponse rendering the paginated list of comments.
    """
    # Проверка наличия параметров `sort_by` и `order`
    if 'sort_by' not in request.GET and 'order' not in request.GET:
        base_url = reverse('comment_list')
        query_string = '?sort_by=created_at&order=desc'
        return redirect(base_url + query_string)
    comments = get_sorted_comments(request)
    # пагинатор
    comments_paginator = Paginator(comments, 25)
    paginator_number = request.GET.get('page')
    try:
        comments_page = comments_paginator.page(paginator_number)
    except PageNotAnInteger:
        # Если номер страницы не является целым числом, показываем первую
        # страницу
        comments_page = comments_paginator.page(1)
    except EmptyPage:
        # Если номер страницы выходит за пределы, показываем последнюю страницу
        comments_page = comments_paginator.page(comments_paginator.num_pages)
    return render(request,
                  'comments/comment_list.html',
                  {'comments': comments_page})


@login_required(login_url='login')
def comment_create(request, parent_id=None):
    """
    Creates a new comment, optionally as a reply to an existing comment.

    Handles both GET (form display) and POST (form submission) requests,
    and saves uploaded files associated with the comment.

    Args:
        request: The HTTP request object.
        parent_id: Optional ID of the parent comment if the comment is a reply.

    Returns:
        HTTPResponse rendering the comment form or redirecting to the comment list.
    """
    if request.method == 'POST':
        form = CommentForm(request.POST)
        # если запрос POST отправленна форма
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
                file_type = 'image' if file.content_type.startswith(
                    'image') else 'document'
                File.objects.create(
                    filetype=file_type,
                    filepath=file,
                    comment=comment)
            return redirect('comment_list')
    # Если GET-запрос (просто отображение формы)
    else:
        form = CommentForm()
    return render(request, 'comments/creat_comment.html', {'form': form})


@login_required(login_url='login')
def comment_update(request, comment_id):
    """
    Updates an existing comment with new data.

    Args:
        request: The HTTP request object.
        comment_id: ID of the comment to be updated.

    Returns:
        HTTPResponse rendering the update form or redirecting to the comment list.
    """
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
    """
    Deletes a specific comment.

    Args:
        request: The HTTP request object.
        comment_id: ID of the comment to be deleted.

    Returns:
        HTTPResponse confirming deletion or redirecting to the comment list.
    """
    comment = Comment.objects.get(id=comment_id)
    if request.method == 'POST':
        comment.delete()
        return redirect('comment_list')
    return render(request,
                  'comments/delete_comment.html',
                  {'comment': comment})


def preview_comment(request):  # проверяем валидацию на стороне сервера
    """
    Provides a preview of a comment without saving, using server-side validation.

    Renders the preview HTML and returns it as a JSON response.

    Args:
        request: The HTTP request object, expecting a POST request with comment text.

    Returns:
        JsonResponse with preview HTML or error if the request is invalid.
    """
    if request.method == "POST":
        text = request.POST.get("text", "")
        user = request.user
        context = {
            "text": text,
            "user": user,
        }
        preview_html = render_to_string(
            "comments/preview_comment.html", context)
        return JsonResponse({"preview": preview_html})
    return JsonResponse({"error": "Invalid request"}, status=400)
