"""Сериализаторы приложения 'api'."""
from datetime import datetime

from django.db.models import Avg
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from rest_framework.validators import UniqueTogetherValidator
from reviews.models import Categories, Comments, Genres, Review, Title


class CategoriesSerializer(serializers.ModelSerializer):
    """Сериализатор для категорий."""

    class Meta:
        model = Categories
        fields = ('name', 'slug')


class GenresSerializer(serializers.ModelSerializer):
    """Сериализатор для жанров."""

    class Meta:
        model = Genres
        fields = ('name', 'slug')


class TitleSerializer(serializers.ModelSerializer):
    """Сериализатор для создания, обновления и удаления произведений."""
    category = SlugRelatedField(slug_field='slug',
                                queryset=Categories.objects.all())
    genre = SlugRelatedField(slug_field='slug', many=True,
                             queryset=Genres.objects.all())

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'description', 'genre', 'category')
        validators = [
            UniqueTogetherValidator(
                queryset=Title.objects.all(),
                fields=('name', 'year', 'category'),
                message='Произведение уже существует!'
            )
        ]

    def validate_year(self, value):
        """Валидатор для поля года выпуска. Год выпуска - не больше текущего"""
        year = datetime.now().year
        if value > year:
            raise serializers.ValidationError(
                'Год выпуска не может быть больше текущего!'
            )
        return value


class TitleROSerializer(serializers.ModelSerializer):
    """Сериализатор для чтения произведений."""
    category = CategoriesSerializer(read_only=True)
    genre = GenresSerializer(read_only=True, many=True)
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'rating', 'description', 'genre',
                  'category')

    def get_rating(self, obj):
        """Функция для создания вычисляемого поля 'Рейтинг' произведения."""
        rating = Review.objects.filter(
            title_id=obj.id
        ).aggregate(Avg("score"))["score__avg"]
        if rating:
            return round(rating)
        return None


class ReviewSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(read_only=True, slug_field='username')

    class Meta:
        fields = ('id', 'text', 'author', 'score', 'pub_date',)
        read_only_fields = ('title',)
        model = Review


class CommentSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(read_only=True, slug_field='username')

    class Meta:
        fields = ('id', 'text', 'author', 'pub_date',)
        read_only_fields = ('review_id)',)
        model = Comments
