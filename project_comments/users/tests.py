from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model


User = get_user_model()


class UsersURLTests(TestCase):

    def setUp(self):
        # Создаём пользователя для тестирования
        self.user = User.objects.create_user(username='testuser', email='testuser@example.com', password='password123')
        self.client.login(username='testuser', password='password123')  # Логинимся в клиенте для тестов

    def test_user_list_page(self):
        response = self.client.get(reverse('users_list'))
        self.assertEqual(response.status_code, 200)

    def test_user_registration(self):
        response = self.client.post(reverse('register'), {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password1': 'newpassword123',
            'password2': 'newpassword123',
        })
        self.assertEqual(response.status_code, 302)  # Перенаправление после успешной регистрации
        self.assertTrue(User.objects.filter(username='newuser').exists())  # Проверка, что пользователь был создан

    def test_user_login(self):
        response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'password123',
        })
        self.assertEqual(response.status_code, 302)  # Перенаправление после успешного входа
