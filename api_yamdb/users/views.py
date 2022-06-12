from rest_framework import viewsets, permissions

from .serializers import UserSerializer, User,  UserRegistrationSerializer
from .mixins import OnlyPostModelViewSet


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """Вьюсет пользователя.
    Унаследован от ReadOnlyModelViewSet.
    Чтобы пользователи не могли изменять данные друг друга
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserRegistrationViewSet(OnlyPostModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = (permissions.AllowAny,)
