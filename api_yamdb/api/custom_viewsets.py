"""Кастомные представления приложения 'api'."""
from rest_framework import viewsets, mixins


class ListCreateDeleteViewSet(mixins.ListModelMixin, mixins.CreateModelMixin,
                              mixins.DestroyModelMixin,
                              viewsets.GenericViewSet):
    """Кастомное представление для листинга, создания и удаления записей."""
    pass
