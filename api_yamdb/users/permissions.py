"""Разрешения для работы с пользователями."""
from rest_framework import permissions


class OnlyAdminOrModerator(permissions.BasePermission):
    """Зона управления пользователями для админов и модераторов."""
    def has_permission(self, request, view):
        return (
            request.user.role == "admin"
            or request.user.role == "moderator"
        )


class OnlyAdminCanGiveRole(permissions.BasePermission):
    """Поле role может менять себе и другием только админ."""
    def has_permission(self, request, view,):
        return (
            request.data.get('role')
            and request.user.role == 'admin'
            or (not request.data.get('role'))
        )
