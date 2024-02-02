import base64
from djoser.serializers import UserSerializer
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


class UserGetSerializer(UserSerializer):
    """Гет сериализатор для работы с пользователями ."""

    is_subscribed = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "username",
            "first_name",
            "last_name",
            "is_subscribed",
        )

    def get_is_subscribed(self, following):
        """Проверка на наличие подписки."""
        request = self.context.get("request")
        return (
            request
            and request.user.is_authenticated
            and request.user.follower.filter(following=following).exists()
        )


class PostSerializer(serializers.ModelSerializer):
    blog = serializers.PrimaryKeyRelatedField(queryset=Blog.objects.all(), write_only=True)
    # blog = SlugRelatedField(slug_field='username', read_only=True)
    is_readed = serializers.SerializerMethodField(read_only=True)
    image = Base64ImageField()

    def get_is_readed(self, obj):
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
            "blog",
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


class FollowSerializer(UserGetSerializer):
    """Сериализатор для гет подписок."""

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
    
    def to_representation(self, instance):
        request = self.context.get("request")
        return UserGetSerializer(
            instance.following, context={"request": request}
        ).data