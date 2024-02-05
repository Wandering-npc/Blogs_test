from django.conf import settings
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from rest_framework import permissions, generics
from rest_framework import viewsets, filters, mixins
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from djoser.views import UserViewSet
from rest_framework import status
from rest_framework.decorators import action

from api.pagination import PostPagination
from blogs.models import Follow, Post, Blog, User, UserPostRead
from .serializers import (
    BlogPostsSerializer,
    FollowSerializer,
    PostSerializer,
    BlogSerializer,
    CommentSerializer,
    UserGetSerializer
)
from .permissions import IsAuthorOrReadOnly

class FollowViewSet(UserViewSet):
    """Джосер вьюсет для работы с пользователями."""

    queryset = User.objects.all()
    serializer_class = UserGetSerializer
    permission_classes = [IsAuthorOrReadOnly]

    @action(
        detail=True,
        methods=["POST"],
        permission_classes=[permissions.IsAuthenticated],
    )
    def subscribe(self, request, id):
        """Подписка и отписка от авторов."""
        following = get_object_or_404(User, id=id)
        serializer = FollowSerializer(
            data={"user": request.user.id, "following": following.id},
            context={"request": request},
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @subscribe.mapping.delete
    def unsubscribe(self, request, id):
        get_object_or_404(Follow, user=request.user, following_id=id).delete()
        return Response("Отписан", status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=False,
        permission_classes=[permissions.IsAuthenticated],
    )
    def subscriptions(self, request):
        """Отображение подписок пользователя."""
        queryset = User.objects.filter(following__user=request.user)
        pages = self.paginate_queryset(queryset)
        serializer = FollowSerializer(
            pages, many=True, context={"request": request}
        )
        return self.get_paginated_response(serializer.data)


class PostViewSet(viewsets.ModelViewSet):
    """Вью для постов."""
    # filter_backends = [DjangoFilterBackend]
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [
        IsAuthorOrReadOnly,
        permissions.IsAuthenticated]
    pagination_class = PostPagination
    
    def perform_create(self, serializer):
        blog = Blog.objects.get(user=self.request.user)
        serializer.save(blog=blog)

    def get_queryset(self):
        user = self.request.user
        subscribed_blogs = Follow.objects.filter(user=user).values_list(
            'following__blog',
            flat=True,
        )
        queryset = Post.objects.filter(
            blog_id__in=subscribed_blogs).order_by('-pub_date')
        return queryset[:500]

    def get_object(self):
        queryset = Post.objects.all()
        obj = queryset.get(pk=self.kwargs['pk'])
        self.check_object_permissions(self.request, obj)
        return obj

    @action(
        detail=True,
        methods=['post'],
        permission_classes=[permissions.IsAuthenticated]
    )
    def mark_as_read(self, request, pk=None):
        user = request.user
        post = self.get_object()
        UserPostRead.objects.get_or_create(user=user, post=post)
        return Response("Прочитан", status=status.HTTP_200_OK)

    @mark_as_read.mapping.delete
    def unmark_as_read(self, request, pk=None):
        post = self.get_object()
        get_object_or_404(UserPostRead, user=request.user, post=post).delete()
        return Response("Не прочитан", status=status.HTTP_204_NO_CONTENT)
    
    @action(
        detail=False,
        methods=['get'],
    )
    def by_blog(self, request, id=None):
        if id:
            queryset = Post.objects.filter(blog_id=id).order_by('-pub_date')
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)
        else:
            return Response({"error": "ID не передан"}, status=status.HTTP_400_BAD_REQUEST)


class BlogViewSet(viewsets.ReadOnlyModelViewSet):
    """Вью для блогов."""
    serializer_class = BlogPostsSerializer
    queryset = Blog.objects.all()


class CommentViewSet(viewsets.ModelViewSet):
    """Вью для коментов."""
    serializer_class = CommentSerializer
    permission_classes = (
        IsAuthorOrReadOnly)

    def get_queryset(self):
        post = get_object_or_404(Post, pk=self.kwargs.get('post_id'))
        return post.comments.all()

    def perform_create(self, serializer):
        post = get_object_or_404(Post, pk=self.kwargs.get('post_id'))
        blog = get_object_or_404(Blog, pk=self.request.user.pk)
        serializer.save(blog=blog, post=post)