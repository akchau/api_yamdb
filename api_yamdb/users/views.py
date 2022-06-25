"""Вьюсеты приложения user."""
from json import dumps

from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import filters, status, viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import AccessToken

from .permissions import OnlyAdminOrModerator, OnlyAdminCanGiveRole
from .serializers import (RegistrationSerializer,
                          TokenSerializer,
                          UserSerializer)

User = get_user_model()


class RegisterView(APIView):"""Сериализаторы для модели пользователя."""
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
        if value.lower() == "me":
            raise serializers.ValidationError(
                "Использовать имя 'me' в качестве username запрещено."
            )
        return value


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
    """
    Класс создает пользователя и
    отправляет ему на почту код подтверждения.
    """
    permission_classes = (AllowAny, )

    def post(self, request):
        """Метод для пост-запроса."""
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            username = serializer.validated_data['username']
            user = get_object_or_404(User, username=username)
            confirmation_code = default_token_generator.make_token(user)
            body = {
                "username": username,
                "confirmation_code": confirmation_code
            }
            json_body = dumps(body)
            send_mail(
                subject="Подтверждение регистрации на сайте yamDB",
                message=(
                    f"Добрый день, {username}!\n"
                    f"Для подтверждения регистрации отправьте POST "
                    f"запрос на http://127.0.0.1:8000/api/v1/auth/token/ "
                    f"в теле запроса передайте:\n"
                    f"{json_body}"
                ),
                from_email="pass_confirm_yamdb@yamdb.ya",
                recipient_list=[request.data["email"]],
            )
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TokenView(APIView):
    """Класс получения токена."""
    permission_classes = (AllowAny, )

    def post(self, request):
        """Получение токена при POST-запросе."""
        serializer = TokenSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            user = get_object_or_404(User, username=username)
            if default_token_generator.check_token(
                user, serializer.validated_data['confirmation_code']
            ):
                token = AccessToken.for_user(user)
        return Response({"token": str(token)}, status.HTTP_200_OK)


class UserViewSet(viewsets.ModelViewSet):
    """
    Вью-сет для работы с пользователем.
    Только для админа.
    """

    permission_classes = (OnlyAdminOrModerator, OnlyAdminCanGiveRole, )
    serializer_class = UserSerializer
    queryset = User.objects.all()
    lookup_field = "username"
    filter_backends = (filters.SearchFilter,)
    search_fields = ("username",)
    pagination_class = PageNumberPagination


class UserMeView(APIView):
    """
    Вью-класс для работы с данными пользователя.
    """
    permission_classes = (OnlyAdminCanGiveRole, )

    def get(self, request):
        """Функция возвращает данные пользователя."""
        username = request.user.username
        user = get_object_or_404(User, username=username)
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def patch(self, request):
        """Функция апдейтит данные пользователя, если они валидны."""
        user = get_object_or_404(User, id=1)
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
