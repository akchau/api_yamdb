"""Вьюсеты приложения user."""
from django.shortcuts import get_object_or_404

from rest_framework.response import Response
from rest_framework import viewsets, views, status

from .models import User
from .serializers import UserSerializer, UserMeSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    Вью-сет для работы с пользователем.
    Только для админа.
    """

    serializer_class = UserSerializer
    queryset = User.objects.all()


class UserMeView(views.APIView):
    """
    Вью-сет для работы с данными пользователя.
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
