"""Сериализаторы приложения 'api'."""
from datetime import datetime

from django.db.models import Avg
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from rest_framework.validators import UniqueTogetherValidator

from users.models import User
from reviews.models import Review, Comments, Categories, Genres, Titles


class UserActivationSerializer(serializers.ModelSerializer):
    """
    Сериализатор для создания неподтвержденного пользователя.
    Управление пользователем. Отправка эмэйла.
    """

    class Meta:
        model = User
        fields = ("email", "username")


class UserRegistrationSerializer(serializers.ModelSerializer):
    """
    Сериализатор для регистрации пользователя.
    """

    class Meta:
        fields = ("email", "username")
        model = User


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для админа. Управление пользователем."""

    class Meta:
        model = User
        fields = ("username", "email", "first_name", "last_name", "bio", "role")


class UserMeSerializer(serializers.ModelSerializer):
    """Сериализатор для просмотра и редактирования своих данных."""

    class Meta:
        model = User
        fields = ("username", "email", "first_name", "last_name", "bio", "role")


class ReviewSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(read_only=True, slug_field='username')

    class Meta:
        fields = '__all__'
        read_only_fields = ('title_id',)
        model = Review


class CommentSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(read_only=True, slug_field='username')

    class Meta:
        fields = '__all__'
        read_only_fields = ('review_id',)
        model = Comments


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


class TitlesSerializer(serializers.ModelSerializer):
    """Сериализатор для создания, обновления и удаления произведений."""
    category = SlugRelatedField(slug_field='slug',
                                queryset=Categories.objects.all())
    genre = SlugRelatedField(slug_field='slug', many=True,
                             queryset=Genres.objects.all())

    class Meta:
        model = Titles
        fields = ('id', 'name', 'year', 'description', 'genre', 'category')
        validators = [
            UniqueTogetherValidator(
                queryset=Titles.objects.all(),
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


class TitlesROSerializer(serializers.ModelSerializer):
    """Сериализатор для чтения произведений."""
    category = CategoriesSerializer(read_only=True)
    genre = GenresSerializer(read_only=True, many=True)
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Titles
        fields = ('id', 'name', 'year', 'rating', 'description', 'genre',
                  'category')

    def get_rating(self, obj):
        """Функция для создания вычисляемого поля 'Рейтинг' произведения."""
        avg_score = obj.reviews.aggregate(Avg('score'))['score__avg']
        if avg_score is not None:
            avg_score = round(avg_score)
        return avg_score
