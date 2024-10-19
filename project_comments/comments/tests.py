from django.test import TestCase
from django.urls import reverse


class CommentsURLTests(TestCase):
    def test_comment_list_page(self):
        response = self.client.get(reverse('comment_list'))
        self.assertEqual(response.status_code, 200)
