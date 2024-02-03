from celery import shared_task
from django.template.loader import render_to_string
from django.utils.timezone import now
from blogs.models import Post

@shared_task
def send_email_digest():
    # Получите последние 5 постов за последние 24 часа
    latest_posts = Post.objects.order_by('-pub_date')[:5]

    # Соберите контекст для шаблона письма
    context = {
        'latest_posts': latest_posts,
    }
    message = render_to_string('email_digest.txt', context)
    print(message)