"""Вьюсеты приложения user."""
from json import dumps

from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import AccessToken

from .permissions import OnlyAdmin
from .serializers import (RegistrationSerializer, TokenSerializer,
                          UserSerializer)

User = get_user_model()


@api_view(['POST'])
@permission_classes([AllowAny])
def register_view(request):
    """
    Функция создает пользователя и
    отправляет ему на почту код подтверждения.
    """
    serializer = RegistrationSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
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


class TokenView(APIView):
    """Класс получения токена."""
    permission_classes = (AllowAny, )

    def post(self, request):
        """Получение токена при POST-запросе."""
        serializer = TokenSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True) and serializer.data:
            username = serializer.validated_data['username']
            user = get_object_or_404(User, username=username)
            if default_token_generator.check_token(
                user, serializer.validated_data['confirmation_code']
            ):
                token = AccessToken.for_user(user)
                return Response({"token": str(token)}, status.HTTP_200_OK)
        return Response("Пустой запрос", status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    """
    Вью-сет для работы с пользователем.
    Только для админа.
    """

    permission_classes = (OnlyAdmin, )
    serializer_class = UserSerializer
    queryset = User.objects.all()
    lookup_field = "username"
    filter_backends = (filters.SearchFilter,)
    search_fields = ("username",)
    pagination_class = PageNumberPagination

    @action(detail=False, methods=['get', 'patch'])
    def me(self, request):
        username = request.user.username
        user = get_object_or_404(User, username=username)
        if request.method == 'PATCH':
            serializer = UserSerializer(user, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
