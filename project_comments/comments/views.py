from django.shortcuts import render
from .models import Comment


def comment_list(request):
    # request содержит информацию о запросе
    comments = Comment.objects.all()
    return render(request, 'comments/comment_list.html', {'comments': comments})
