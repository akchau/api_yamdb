"""Разрешения приложения 'api'."""
from django.contrib.auth import get_user_model
from rest_framework import permissions

User = get_user_model()


class AdminOrReadOnly(permissions.BasePermission):
    """Разрешения для чтения записей любым пользователем и создания,
    изменения и удаления записей администратором и суперпользователем."""

    def has_permission(self, request, view):
        """Функция разрешений на уровне запроса."""
        return (request.method in permissions.SAFE_METHODS
                or (request.user.is_authenticated
                    and (request.user.role == 'admin'
                         or request.user.role == 'superuser'))
                )


class AuthorOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or obj.author == request.user
            or request.user.role == 'admin'
            or request.user.role == 'moderator'
        )
