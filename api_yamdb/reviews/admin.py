"""Админка приложения 'reviews'."""
from django.contrib import admin

from .models import Categories, Genres, Titles, GenreTitle, Review, Comments


class CategoriesAdmin(admin.ModelAdmin):
    """Админка категорий."""
    list_display = ('id', 'name', 'slug',)
    search_fields = ('name',)
    list_filter = ('slug',)
    empty_value_display = '-пусто-'


class GenresAdmin(admin.ModelAdmin):
    """Админка жанров."""
    list_display = ('id', 'name', 'slug',)
    search_fields = ('name',)
    list_filter = ('slug',)
    empty_value_display = '-пусто-'


class TitlesAdmin(admin.ModelAdmin):
    """Админка произведений."""
    list_display = ('id', 'name', 'year', 'description', 'category',)
    list_editable = ('category',)
    search_fields = ('name',)
    list_filter = ('year',)
    empty_value_display = '-пусто-'


class GenreTitleAdmin(admin.ModelAdmin):
    """Админка произведений и жанров."""
    list_display = ('id', 'title_id', 'genre_id',)
    list_editable = ('title_id', 'genre_id',)
    empty_value_display = '-пусто-'


class ReviewAdmin(admin.ModelAdmin):
    """Админка ревью."""
    list_display = ('id', 'title_id', 'text', 'author', 'score', 'pub_date',)
    list_editable = ('title_id', 'author',)
    search_fields = ('text',)
    list_filter = ('author',)
    empty_value_display = '-пусто-'


class CommentsAdmin(admin.ModelAdmin):
    """Админка комментариев."""
    list_display = ('id', 'review_id', 'text', 'author', 'pub_date',)
    list_editable = ('review_id', 'author',)
    search_fields = ('text',)
    list_filter = ('author',)
    empty_value_display = '-пусто-'


admin.site.register(Categories, CategoriesAdmin)
admin.site.register(Genres, GenresAdmin)
admin.site.register(Titles, TitlesAdmin)
admin.site.register(GenreTitle, GenreTitleAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Comments, CommentsAdmin)
