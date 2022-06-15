from django.shortcuts import get_object_or_404
from django.core.mail import send_mail
from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from .permissions import OnlyMe
from .serializers import UserSerializer, User


class RegistrationAPIView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        email = self.validated_data["email"]
        send_mail(
            "Подтверждение регистрации yamdb",
            "Для подтверждения регистрации перейдите сделайте запрос на.",
            "yamdb@yamdb.com",
            [email],
            fail_silently=False,
        )
        return Response(self.serializer.data)


class UserViewSet(viewsets.ModelViewSet):
    """Вьюсет пользователя.
    Унаследован от ModelViewSet.
    Чтобы пользователи не могли изменять данные друг друга
    """

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAdminUser,)


class UserMeApi(APIView):
    permission_classes = (OnlyMe, permissions.IsAuthenticated)

    def get(self, request):
        queryset = User.objects.all()
        user = get_object_or_404(queryset, username=request.user.username)
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def patch(self, request):
        queryset = User.objects.all()
        user = get_object_or_404(queryset, username=request.user.username)
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data)
