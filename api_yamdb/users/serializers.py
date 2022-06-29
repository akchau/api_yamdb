"""Сериализаторы для модели пользователя."""
from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class RegistrationSerializer(serializers.ModelSerializer):
    """
    Сериализатор для создания неподтвержденного польлзователя.
    Управление пользователем. Отправка эмэйла."
    """

    class Meta:
        model = User
        fields = ("email", "username")

    def validate_username(self, value):
        """Проверка username !=me"""
        try:
            User.objects.get(username=value)
        except User.DoesNotExist:
            if value.lower() == "me":
                raise serializers.ValidationError(
                    "Использовать имя 'me' в качестве username запрещено."
                )
            return value
        raise serializers.ValidationError('Пользователь существует.')

    def validate_email(self, value):
        try:
            User.objects.get(email=value)
        except User.DoesNotExist:
            return value
        raise serializers.ValidationError('Пользователь существует.')


class TokenSerializer(serializers.Serializer):
    """Сериализатор для авторизации пользователя."""
    username = serializers.CharField(max_length=255)
    confirmation_code = serializers.CharField(max_length=128)


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор управления пользователем."""

    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "first_name",
            "last_name",
            "bio",
            "role"
        )
