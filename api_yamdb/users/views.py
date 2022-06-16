"""Вьюсеты приложения user."""
from django.shortcuts import get_object_or_404
from django.core.mail import send_mail
from rest_framework.response import Response
from rest_framework import viewsets, status, permissions
from rest_framework.views import APIView

from .models import User
from .serializers import UserSerializer, UserMeSerializer, UserActivationSerializer


class UserActivationView(APIView):
    """Вью-класс для создания пользователя."""
    # permission_classes = ['AllowAny', ]

    def post(self, request):
        """Метод для пост-запроса."""
        serializer = UserActivationSerializer(data=request.data)
        confirmation_code = 'hi'
        if serializer.is_valid():
            username = request.data['username']
            send_mail(
                subject='Подтверждение регистрации на сайте yamDB',
                message=(f'Добрый день, {username}!\n'
                         f'Для подтверждения регистрации отправьте POST '
                         f'запрос на http://127.0.0.1:8000/api/v1/auth/token/ '
                         f'в теле запроса передайте:\n'
                         '{\n'
                         f'  "username": "{username}",\n'
                         f'  "confirmation_code": "{confirmation_code}"\n'
                         '}'),
                from_email='pass_confirm_yamdb@yamdb.ya',
                recipient_list=[request.data['email']],
                fail_silently=False,
                auth_user=None,
                auth_password=None,
                connection=None,
                html_message=None
            )
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    """
    Вью-сет для работы с пользователем.
    Только для админа.
    """
    # permission_classes = [permissions.IsAdminUser]
    serializer_class = UserSerializer
    queryset = User.objects.all()
    lookup_field = 'username'


class UserMeView(APIView):
    """
    Вью-класс для работы с данными пользователя.
    """

    def get(self, request):
        """Функция возвращает данные пользователя."""
        user = get_object_or_404(User, id=1)
        serializer = UserMeSerializer(user)
        return Response(serializer.data)

    def patch(self, request):
        """Функция апдейтит данные пользователя, если они валидны."""
        user = get_object_or_404(User, id=1)
        serializer = UserMeSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
