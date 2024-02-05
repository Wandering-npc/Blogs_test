from django.urls import include, path
from rest_framework.routers import DefaultRouter


from api.views import (
    CommentViewSet,
    PostViewSet,
    BlogViewSet,
    FollowViewSet,
)

app_name = 'api'

router = DefaultRouter()
router.register(r'posts', PostViewSet, basename='posts')
router.register(
    r'posts/(?P<post_id>\d+)/comments', CommentViewSet, basename='comments'
)
router.register(r'blogs', BlogViewSet, basename='blogs')
router.register(r"users", FollowViewSet, basename="users")


urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/', include('djoser.urls')),
    # path('v1/api/blogs/<int:id>/posts/', PostViewSet.as_view({'get': 'by_blog'}), name='posts-by-blog'),
    path("auth/", include("djoser.urls.authtoken")),
]