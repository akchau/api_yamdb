"""Разрешения для работы с пользователями."""
from rest_framework import permissions


class OnlyAdmin(permissions.BasePermission):
    """Зона управления пользователями для админов и модераторов."""
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and 
            request.user.role == "admin"
        )


class OnlyAdminCanGiveRole(permissions.BasePermission):
    """Поле role может менять себе и другием только админ."""
    def has_permission(self, request, view,):
        return (
            request.method in permissions.SAFE_METHODS
            or request.data.get('role')
            and request.user.role == 'admin'
            or (not request.data.get('role'))
        )


class OnlyUser(permissions.BasePermission):
    """Только для юзеров."""
    def has_permission(self, request, view,):
        return (
            request.user.role == 'user'
        )
