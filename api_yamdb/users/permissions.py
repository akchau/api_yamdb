"""Разрешения для работы с пользователями."""
from rest_framework import permissions
from rest_framework.views import exceptions


class OnlyAdmin(permissions.BasePermission):
    """Зона управления пользователями для админов."""
    def has_permission(self, request, view):
        return (
            request.user.is_superuser
            or (request.user.is_authenticated
                and request.user.role == "admin")
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
            raise exceptions.NotAuthenticated(detail={"role": 'user'})


class OnlyUser(permissions.BasePermission):
    """Только для юзеров."""
    def has_permission(self, request, view,):
        return (
            request.user.role == 'user'
        )
