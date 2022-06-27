"""Разрешения для работы с пользователями."""
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import exceptions


class OnlyAdmin(permissions.BasePermission):
    """Зона управления пользователями для админов и модераторов."""
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.role == "admin"
        )


class OnlyAdminCanGiveRole(permissions.BasePermission):
    """Поле role может менять себе и другием только админ."""
    def has_permission(self, request, view,):
        if request.user.is_anonymous:
            raise exceptions.NotAuthenticated()
        if (
            request.method in permissions.SAFE_METHODS
            or request.data.get('role')
            and request.user.role == 'admin'
            or (not request.data.get('role'))
        ):
            return True
        else:
            _mutable = request.data._mutable
            request.data._mutable = True
            request.data['role'] = 'user'
            request.data._mutable = _mutable
            return Response(None, status=status.HTTP_403_FORBIDDEN)


class OnlyUser(permissions.BasePermission):
    """Только для юзеров."""
    def has_permission(self, request, view,):
        return (
            request.user.role == 'user'
        )
