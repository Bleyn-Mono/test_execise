from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Comment


User = get_user_model()


class CommentsURLTests(TestCase):

    def setUp(self):
        # Создаём пользователя для тестов
        self.user = User.objects.create_user(username='testuser', email='testuser@example.com', password='password123')
        self.client.login(username='testuser', password='password123')  # Логинимся в клиенте для тестов
        # Создаём тестовый комментарий
        self.comment = Comment.objects.create(user=self.user, text="Test comment")

    def test_comment_list_page(self):
        response = self.client.get(reverse('comment_list'))
        self.assertEqual(response.status_code, 200)

    def test_create_comment(self):
        response = self.client.post(reverse('comment_create'), {'user_name': 'testuser', 'email': 'testuser@example.com',
            'text': 'New test comment',
        })
        self.assertEqual(response.status_code, 302)  # Перенаправление после создания
        self.assertTrue(Comment.objects.filter(text='New test comment').exists())  # Проверка, что комментарий был создан

    def test_update_comment(self):
        # Изменяем комментарий
        response = self.client.post(reverse('update_comment', args=[self.comment.id]), {'user_name': 'testuser', 'email': 'testuser@example.com',
            'text': 'Updated comment text',
        })
        self.assertEqual(response.status_code, 302)  # Перенаправление после редактирования
        self.comment.refresh_from_db()
        self.assertEqual(self.comment.text, 'Updated comment text')  # Проверка изменения текста комментария

    def test_delete_comment(self):
        # Удаляем комментарий
        response = self.client.post(reverse('delete_comment', args=[self.comment.id]))
        self.assertEqual(response.status_code, 302)  # Перенаправление после удаления
        self.assertFalse(Comment.objects.filter(id=self.comment.id).exists())  # Проверка, что комментарий был удалён
