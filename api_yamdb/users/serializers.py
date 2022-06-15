from django.contrib.auth import get_user_model
from rest_framework import serializers


User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("username", "email", "first_name", "last_name", "bio", "role")


class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ("email", "username")
        model = User

    def validate_username(self, value):
        if value == "me":
            raise serializers.ValidationError("Недоступное имя пользователя")
        return value
