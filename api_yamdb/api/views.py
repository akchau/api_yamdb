"""Представления приложения 'api'."""
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Avg
from rest_framework import filters, viewsets
from rest_framework.exceptions import ParseError
from rest_framework.pagination import LimitOffsetPagination

from reviews.models import Categories, Comments, Genres, Review, Title
from users.models import CustomUser as User
from .custom_viewsets import ListCreateDeleteViewSet
from .filters import TitleFilter
from .permissions import AdminOrReadOnly, AuthorOrReadOnly
from .serializers import (CategoriesSerializer, CommentSerializer,
                          GenresSerializer, ReviewSerializer,
                          TitleROSerializer, TitleSerializer)


def get_usr(self):
    return get_object_or_404(
        User,
        username=self.request.user,
    )


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


class TitleViewSet(viewsets.ModelViewSet):
    """Представление для работы с произведениями."""
    queryset = Title.objects.all().annotate(Avg("review__score")).order_by(
        "id")
    serializer_class = TitleSerializer
    permission_classes = (AdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter

    def get_serializer_class(self):
        """Функция выбора сериализатора."""
        if self.action in ('list', 'retrieve'):
            return TitleROSerializer
        return TitleSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (AuthorOrReadOnly,)

    def get_queryset(self):
        url_title_id = self.kwargs.get("url_title_id")
        return Review.objects.filter(title_id=url_title_id)

    def perform_create(self, serializer):
        obj = ""
        title = get_object_or_404(
            Title,
            id=self.kwargs.get("url_title_id")
        )
        try:
            obj = Review.objects.get(
                title_id=title,
                author=get_usr(self)
            )
        except ObjectDoesNotExist:
            pass
        if obj:
            raise ParseError("Отзыв уже существует!")
        else:
            serializer.save(author=get_usr(self), title=title)


class CommentsViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = (AuthorOrReadOnly,)

    def get_queryset(self):
        url_review_id = self.kwargs.get("url_review_id")
        return Comments.objects.filter(review_id=url_review_id)

    def perform_create(self, serializer):
        review = get_object_or_404(
            Review,
            id=self.kwargs.get("url_review_id")
        )
        serializer.save(author=get_usr(self), review_id=review)
