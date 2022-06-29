"""Разрешения приложения 'api'."""
from rest_framework import permissions


class AdminOrReadOnly(permissions.BasePermission):
    """Разрешения для чтения записей любым пользователем и создания,
    изменения и удаления записей администратором и суперпользователем."""

    def has_permission(self, request, view):
        """Функция разрешений на уровне запроса."""
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.user.is_authenticated:
            if request.user.is_superuser or request.user.is_admin:
                return True
        return False

#        return (request.method in permissions.SAFE_METHODS
#                or (request.user.is_authenticated
#                    and (request.user.role == 'admin'
#                         or request.user.role == 'superuser'))
#                )


class AuthorOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.user.is_authenticated:
            return True
        return False

#        return (
#            request.method in permissions.SAFE_METHODS
#            or request.user.is_authenticated
#        )

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        if (request.user.is_superuser or request.user.is_admin
                or request.user.is_moderator):
            return True
        if obj.author == request.user:
            return True
        return False

#        return (
#            request.method in permissions.SAFE_METHODS
#            or obj.author == request.user
#            or request.user.role == 'admin'
#            or request.user.role == 'moderator'
#        )
