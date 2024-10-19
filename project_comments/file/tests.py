from django.test import TestCase
from django.urls import reverse


class FilesURLTests(TestCase):
    def test_file_list_page(self):
        response = self.client.get(reverse('file_list'))
        self.assertEqual(response.status_code, 200)
