from django.contrib.auth import get_user_model
from djoser.serializers import UserCreateSerializer
from rest_framework import serializers


User = get_user_model()


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role'
        )


class UserRegistrationSerializer(serializers.ModelSerializer):

    class Meta(UserCreateSerializer.Meta):
        fields = ('email', 'username')
        model = User
