from django.shortcuts import render
from .models import File


def file_list(request):
    """
    View function to list all uploaded files.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The rendered HTML response containing the list of files.
    """
    files = File.objects.all()
    return render(request, 'file/file_list.html', {'files': files})
