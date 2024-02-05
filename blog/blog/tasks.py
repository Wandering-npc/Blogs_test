from celery import shared_task
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.contrib.auth.models import User

from blogs.models import Post, Follow
from blog.celery import app

@app.task
def send_email_digest():
    users = User.objects.all()
    count = 0

    for user in users:
        subscribed_blogs = Follow.objects.filter(user=user).values_list(
            'following__blog',
            flat=True,
        )
        posts = Post.objects.filter(blog_id__in=subscribed_blogs)
        latest_posts = posts.order_by('-pub_date')[:5]

        context = {
            'latest_posts': latest_posts,
            'username': user.username,
        }
        count+=1
        message = render_to_string('email_digest.txt', context)
        # print(message)
        print(count)