from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from rest_framework import permissions
from rest_framework import viewsets, filters, mixins
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from djoser.views import UserViewSet
from rest_framework import status
from rest_framework.decorators import action

from blogs.models import Follow, Post, Blog, User
from .serializers import PostSerializer, BlogSerializer, CommentSerializer, UserGetSerializer
from .serializers import FollowSerializer
from .permissions import IsAuthorOrReadOnly

class FollowViewSet(UserViewSet):
    """Джосер вьюсет для работы с пользователями."""

    queryset = User.objects.all()
    serializer_class = UserGetSerializer
    # permission_classes = [AuthorOrReadOnly]

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
    filter_backends = [DjangoFilterBackend]
    # filterset_class = RecipeFilter
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [
        IsAuthorOrReadOnly,
        permissions.IsAuthenticated]
    pagination_class = LimitOffsetPagination


    def list(self, request, *args, **kwargs):
        user = request.user
        subscribed_blogs = Follow.objects.filter(user=user).values_list(
            'following__blog',
            flat=True,
        )
        queryset = self.queryset.filter(blog_id__in=subscribed_blogs)
        queryset = queryset.order_by('-pub_date')[:500]
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def perform_create(self, serializer):
        serializer.save(blog=self.request.user.id)


class BlogViewSet(viewsets.ReadOnlyModelViewSet):
    """Вью для блогов."""
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer


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


# class FollowViewSet(
#     mixins.CreateModelMixin,
#     mixins.ListModelMixin,
#     viewsets.GenericViewSet,
# ):
#     """Вьюсет для подписки."""
#     serializer_class = FollowSerializer
#     permission_classes = [permissions.IsAuthenticated]
#     filter_backends = (filters.SearchFilter,)
#     search_fields = ('following__username', 'user__username')

#     def get_queryset(self):
#         user = get_object_or_404(User, username=self.request.user.username)
#         return user.follower.all()

#     def perform_create(self, serializer):
#         serializer.save(user=self.request.user)
    
#     @action(detail=True, methods=['delete'])
#     def unfollow(self, request, pk=None):
#         get_object_or_404(Follow, user=request.user, author_id=id).delete()
# #         return Response(status=status.HTTP_204_NO_CONTENT)
