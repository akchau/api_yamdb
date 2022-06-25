from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
# from rest_framework.validators import UniqueTogetherValidator
from users.models import User
from reviews.models import Review, Comments
from django.db.models import Avg


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
    score = serializers.SerializerMethodField()

    class Meta:
        fields = ('id', 'text', 'author', 'score', 'pub_date',)
        read_only_fields = ('title_id',)
        model = Review

    def get_score(self, obj):
        return int(
            Review.objects.filter(
                title_id=obj.title_id.id
            ).aggregate(Avg("score"))["score__avg"]
        )


class CommentSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(read_only=True, slug_field='username')

    class Meta:
        fields = ('id', 'text', 'author', 'pub_date',)
        read_only_fields = ('review_id)',)
        model = Comments
