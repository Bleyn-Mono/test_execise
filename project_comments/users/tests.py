from django.test import TestCase
from django.urls import reverse


class UsersURLTests(TestCase):
    def test_user_list_page(self):
        response = self.client.get(reverse('users_list'))
        self.assertEqual(response.status_code, 200)
