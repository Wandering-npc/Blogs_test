from django.db import models
from django.contrib.auth.models import User

class Blog(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)


class Post(models.Model):
    title = models.CharField(max_length=100)
    text = models.TextField(max_length=140)
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)
    image = models.ImageField(
        upload_to='posts/', null=True, blank=True)
    updated = models.DateTimeField(
        verbose_name='Обновлен',
        auto_now=True,
        db_index=True
    )
    blog = models.ForeignKey(
        Blog,
        on_delete=models.CASCADE,
        related_name='posts',
    )

    def __str__(self):
        return self.text


class Comment(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments')
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    created = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True)


class Follow(models.Model):
    """Модель подписки."""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower',
    )
    following = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following',
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'following'], name='unique_follow'
            )
        ]


class UserPostRead(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='readed',
    )
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='readed',
    )

    class Meta:
        verbose_name = 'Прочитанный пост'
        verbose_name_plural = 'Прочитанные посты'
        unique_together = (('user', 'post'),)