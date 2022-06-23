from datetime import datetime

from django.db.models import Avg
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField

from users.models import User
from reviews.models import Review, Comments, Categories, Genres, Titles


class UserActivationSerializer(serializers.ModelSerializer):
    """
    Сериализатор для создания неподтвержденного польлзователя.
    Управление пользователем. Отправка эмэйла."
    """

    class Meta:
        model = User
        fields = ("email", "username")


class UserRegistrationSerializer(serializers.ModelSerializer):
    """
    Сериализатор для регистрации польлзователя."
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

    class Meta:
        model = Categories
        fields = ('name', 'slug')


class GenresSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genres
        fields = ('name', 'slug')


class TitlesSerializer(serializers.ModelSerializer):
    category = SlugRelatedField(slug_field='slug',
                                queryset=Categories.objects.all())
    genre = SlugRelatedField(slug_field='slug', many=True,
                             queryset=Genres.objects.all())

    class Meta:
        model = Titles
        fields = ('id', 'name', 'year', 'description', 'genre', 'category')

    def validate_year(self, value):
        year = datetime.now().year
        if value > year:
            raise serializers.ValidationError(
                'Год выпуска не может быть больше текущего!'
            )
        return value


class TitlesROSerializer(serializers.ModelSerializer):
    category = CategoriesSerializer(read_only=True)
    genre = GenresSerializer(read_only=True, many=True)
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Titles
        fields = ('id', 'name', 'year', 'rating', 'description', 'genre',
                  'category')

    def get_rating(self, obj):
        avg_score = obj.reviews.aggregate(Avg('score'))['score__avg']
        if avg_score is not None:
            avg_score = round(avg_score)
        return avg_score
