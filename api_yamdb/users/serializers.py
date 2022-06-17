"""Сериализаторы для модели пользователя."""

from rest_framework import serializers

from .models import User


class UserActivationSerializer(serializers.ModelSerializer):
    """
    Сериализатор для создания неподтвержденного польлзователя.
    Управление пользователем. Отправка эмэйла."
    """

    class Meta:
        model = User
        fields = ("email", "username")

    def validate_username(self, value):
        """Проверка username !=me"""
        if value == "me":
            raise serializers.ValidationError(
                "Использовать имя 'me' в качестве username запрещено."
            )
        return value

    def validate_email(self, value):
        """Проверка уникальности email."""
        if User.objects.filter(email=value):
            raise serializers.ValidationError("A user with that email already exists.")
        return value


class UserRegistrationSerializer(serializers.ModelSerializer):
    """
    Сериализатор для регистрации польлзователя."
    """

    class Meta:
        fields = ("username", "confirmation_code")
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
