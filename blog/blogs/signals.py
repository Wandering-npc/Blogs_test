from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User, Blog


@receiver(post_save, sender=User)
def create_user_blog(sender, instance, created, **kwargs):
    if created:
        Blog.objects.create(user=instance, name=instance.username)