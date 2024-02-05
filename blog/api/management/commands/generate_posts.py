from django.core.management.base import BaseCommand
from blogs.models import Post, Blog
from django.contrib.auth.models import User
import random
import string

class Command(BaseCommand):
    help = "Генерация постов для тестирования."

    def handle(self, *args, **options):
        titles = ["Заголовок поста " + str(i) for i in range(1, 501)]
        texts = [
            "Текст поста " + ''.join(
            random.choices(
            string.ascii_letters + string.digits, k=20)) for _ in range(500)]
        usernames = ["user" + str(i) for i in range(1, 11)]
        passwords = [
            ''.join(random.choices(
            string.ascii_letters + string.digits, k=10)) for _ in range(10)]

        for i in range(10):
            username = 'user' + str(i)
            password = random.choice(passwords)
            User.objects.create(
                username=username,
                password=password,
            )
        blogs = Blog.objects.all()
        for _ in range(1000):
            title = random.choice(titles)
            text = random.choice(texts)
            blog = random.choice(blogs)
            Post.objects.create(
                title=title,
                text=text,
                blog=blog,
            )

        self.stdout.write(self.style.SUCCESS("Создано 1000 постов"))