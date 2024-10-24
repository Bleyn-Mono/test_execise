from django.urls import path
from . import views


urlpatterns = [
    path ('', views.comment_list, name='comment_list'),
    path('create/', views.comment_create, name='comment_create'),
    path('create/<int:parent_id>', views.comment_create, name='comment_create_with_parent'),
    path('update/<int:comment_id>/', views.comment_update, name='update_comment'),
    path('delete/<int:comment_id>/', views.comment_delete, name='delete_comment'),
]