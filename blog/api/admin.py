from django.contrib import admin
from blogs.models import User, Blog, Post, Follow, UserPostRead

# @admin.register(User)
# class UserAdmin(admin.ModelAdmin):
#     pass

@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    pass

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'blog', 'pub_date')
    list_filter = ('blog', 'pub_date')
    search_fields = ('title', 'blog__user__username')

@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    pass

@admin.register(UserPostRead)
class UserPostReadAdmin(admin.ModelAdmin):
    pass
