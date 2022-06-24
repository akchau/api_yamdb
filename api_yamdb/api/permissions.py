"""Разрешения приложения 'api'."""
from rest_framework import permissions


class OnlyMe(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj == request.user


class AdminOrReadOnly(permissions.BasePermission):
    """Разрешения для чтения записей любым пользователем и создания,
    изменения и удаления записей администратором и суперпользователем."""

    def has_permission(self, request, view):
        """Функция разрешений на уровне запроса."""
        return (
                request.method in permissions.SAFE_METHODS
                or (request.user.is_authenticated
                    and (request.user.role == 'admin'
                         or request.user.role == 'superuser'))
        )
