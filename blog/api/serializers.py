import base64

from django.core.files.base import ContentFile
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField


from blogs.models import Comment, Post, Blog, Follow, User


class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith("data:image"):
            format, imgstr = data.split(";base64,")
            ext = format.split("/")[-1]

            data = ContentFile(base64.b64decode(imgstr), name="temp." + ext)

        return super().to_internal_value(data)
    

class PostSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field='username', read_only=True)
    is_readed = serializers.SerializerMethodField(read_only=True)

    def get_is_favorited(self, obj):
        user = self.context.get("request").user
        if user.is_authenticated:
            return user.readed.filter(post=obj).exists()
        return False
    
    class Meta:
        fields = (
            "title",
            "text",
            "pub_date",
            "image",
            "updated",
            "blog",
            "is_readed",
            "author",
        )
        model = Post


class BlogSerializer(serializers.ModelSerializer):
    """Сериализация blog."""

    class Meta:
        fields = '__all__'
        model = Blog


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        fields = '__all__'
        read_only_fields = ('post',)
        model = Comment


class FollowSerializer(serializers.ModelSerializer):
    """Сериализация подписок"""
    user = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
        default=serializers.CurrentUserDefault())
    following = serializers.SlugRelatedField(
        queryset=User.objects.all(),
        slug_field='username')

    class Meta:
        model = Follow
        fields = '__all__'
        validators = [
            serializers.UniqueTogetherValidator(
                queryset=Follow.objects.all(),
                fields=['user', 'following'],
                message='Вы уже подписаны'
            )
        ]

    def validate_following(self, value):
        if value == self.context['request'].user:
            raise serializers.ValidationError(
                'Нельзя подписаться на себя :('
            )
        return value