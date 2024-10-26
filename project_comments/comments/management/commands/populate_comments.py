# comments/management/commands/populate_comments.py
from django.core.management.base import BaseCommand
from comments.models import Comment
from users.models import User
from faker import Faker
import random

class Command(BaseCommand):
    help = 'Заполняет базу данных фейковыми комментариями'

    def handle(self, *args, **kwargs):
        fake = Faker()
        users = User.objects.all()

        # Убедимся, что в базе есть пользователи
        if not users.exists():
            self.stdout.write(self.style.ERROR('Нет пользователей в базе данных'))
            return

        # Генерируем 100 фейковых комментариев
        for _ in range(100):
            user = random.choice(users)
            text = fake.paragraph(nb_sentences=3)
            parent_comment = Comment.objects.order_by('?').first() if random.choice([True, False]) else None

            Comment.objects.create(
                user=user,
                text=text,
                parent=parent_comment
            )

        self.stdout.write(self.style.SUCCESS('База данных успешно заполнена фейковыми комментариями!'))
