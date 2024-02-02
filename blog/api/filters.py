from django_filters.rest_framework import FilterSet, filters

from blogs.models import Post, Ingredient


class RecipeFilter(FilterSet):
    is_readed = filters.BooleanFilter(
        method="get_is_readed"
    )

    class Meta:
        model = Post
        fields = ("get_is_readed", "blog")

    def get_is_favorited(self, queryset, name, value):
        if self.request.user.is_authenticated and value:
            return queryset.filter(readed__user=self.request.user)
        return queryset