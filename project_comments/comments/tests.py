from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Comment
from .forms import CommentForm
from captcha.models import CaptchaStore


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

class CommentSortingTests(TestCase):
    def setUp(self):
        self.user1 = User.objects.create(username="alice", email="alice@example.com")
        self.user2 = User.objects.create(username="bob", email="bob@example.com")
        self.user3 = User.objects.create(username="charlie", email="charlie@example.com")

        # Создаем комментарии для каждого пользователя
        Comment.objects.create(user=self.user2, text="Bob's comment")
        Comment.objects.create(user=self.user3, text="Charlie's comment")
        Comment.objects.create(user=self.user1, text="Alice's comment")

    def test_sort_by_username(self):
        response = self.client.get(reverse('comment_list') + '?sort_by=username')
        self.assertEqual(response.status_code, 200)
        comments = response.context['comments']
        # Извлекаем имена пользователей из отсортированного списка комментариев
        usernames = [comment.user.username for comment in comments]
        # Проверяем порядок имен пользователей
        self.assertEqual(usernames, ["alice", "bob", "charlie"])

    def test_sort_by_email(self):
        response = self.client.get(reverse('comment_list') + '?sort_by=email')
        self.assertEqual(response.status_code, 200)
        comments = response.context['comments']
        # Извлекаем адреса электронной почты из отсортированного списка комментариев
        emails = [comment.user.email for comment in comments]
        # Проверяем порядок адресов электронной почты
        self.assertEqual(emails, ["alice@example.com", "bob@example.com", "charlie@example.com"])


class CommentPaginationTests(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="paginationuser", email="paginationuser@example.com")
        for i in range(30):  # Создаём 30 комментариев для теста пагинации
            Comment.objects.create(user=self.user, text=f"Comment {i}")

    def test_first_page_contains_25_comments(self):
        response = self.client.get(reverse('comment_list'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['comments']), 25)

    def test_second_page_contains_remaining_comments(self):
        response = self.client.get(reverse('comment_list') + '?page=2')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['comments']), 5)


class CommentFormCaptchaTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="captchatestuser", email="captchatest@example.com")

    def test_captcha_field_in_form(self):
        form = CommentForm()
        self.assertIn('captcha', form.fields) #проверяем что есть поле капчи

    def test_captcha_validation(self):
        captcha = CaptchaStore.objects.create(response="testcaptcha")
        form_data = {
            'user_name': 'testuser',
            'email': 'testuser@example.com',
            'text': 'This is a comment with captcha',
            'captcha_0': captcha.hashkey,
            'captcha_1': 'testcaptcha'
        }
        form = CommentForm(data=form_data)
        self.assertTrue(form.is_valid())