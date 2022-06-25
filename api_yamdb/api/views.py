"""Представления приложения 'api'."""
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend

from users.models import User
from reviews.models import Comments, Review, Categories, Genres, Titles
from rest_framework.pagination import LimitOffsetPagination
from .permissions import AuthorOrReadOnly
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework import viewsets, views, status
from users.models import User
from reviews.models import Comments, Review, Titles
from .serializers import (
    ReviewSerializer,
    CommentSerializer,
    UserSerializer,
    UserMeSerializer,
    CategoriesSerializer,
    GenresSerializer,
    TitlesSerializer,
    TitlesROSerializer
)
from .custom_viewsets import ListCreateDeleteViewSet
from .permissions import AdminOrReadOnly
from .filters import TitleFilter


def get_usr(self):
    return get_object_or_404(
        User,
        username=self.request.user,
    )


class UserViewSet(viewsets.ModelViewSet):
    """
    Вью-сет для работы с пользователем.
    Только для админа.
    """

    serializer_class = UserSerializer
    queryset = User.objects.all()


class UserMeView(viewsets.ModelViewSet):
    """
    Вью-сет для работы с данными пользователя.
    """
    serializer_class = UserMeSerializer

    def get_queryset(self):
        user = self.request.user.id
        return get_object_or_404(User, id=user)


class CategoriesViewSet(ListCreateDeleteViewSet):
    """Представление для работы с категориями."""
    queryset = Categories.objects.all()
    serializer_class = CategoriesSerializer
    permission_classes = (AdminOrReadOnly,)
    lookup_field = 'slug'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class GenresViewSet(ListCreateDeleteViewSet):
    """Представление для работы с жанрами."""
    queryset = Genres.objects.all()
    serializer_class = GenresSerializer
    permission_classes = (AdminOrReadOnly,)
    lookup_field = 'slug'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class TitlesViewSet(viewsets.ModelViewSet):
    """Представление для работы с произведениями."""
    queryset = Titles.objects.all()
    serializer_class = TitlesSerializer
    permission_classes = (AdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter

    def get_serializer_class(self):
        """Функция выбора сериализатора."""
        if self.action in ('list', 'retrieve'):
            return TitlesROSerializer
        return TitlesSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    # permission_classes = (AuthorOrReadOnly,)

    def get_queryset(self):
        url_title_id = self.kwargs.get("url_title_id")
        return Review.objects.filter(title_id=url_title_id)

    def perform_create(self, serializer):
        title = get_object_or_404(
            Titles,
            id=self.kwargs.get("url_title_id")
        )
        serializer.save(author=get_usr(self), title_id=title)


class CommentsViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    pagination_class = LimitOffsetPagination
    # permission_classes = (AuthorOrReadOnly,)

    def get_queryset(self):
        url_review_id = self.kwargs.get("url_review_id")
        return Comments.objects.filter(review_id=url_review_id)

    def perform_create(self, serializer):
        review = get_object_or_404(
            Review,
            id=self.kwargs.get("url_review_id")
        )
        serializer.save(author=get_usr(self), review_id=review)
