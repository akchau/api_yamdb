"""Представления приложения 'api'."""
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend

from users.models import User
from reviews.models import Comments, Review, Categories, Genres, Titles
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

    # def get(self, request):
    #     """Функция возвращает данные пользователя."""
    #     user = get_object_or_404(User, id=1)
    #     serializer = UserMeSerializer(user)
    #     return Response(serializer.data)

    # def patch(self, request):
    #     """Функция апдейтит данные пользователя, если они валидны."""
    #     user = get_object_or_404(User, id=1)
    #     serializer = UserMeSerializer(user, data=request.data, partial=True)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_200_OK)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    # permission_classes = (AuthorOrReadOnly,)

    def get_queryset(self):
        url_title_id = self.kwargs.get("url_title_id")
        return Comments.objects.filter(title_id=url_title_id)

    def perform_create(self, serializer):
        author = self.request.user
        review = get_object_or_404(
            Review,
            id=self.kwargs.get("url_title_id")
        )
        serializer.save(author=author, title_id=review)


class CommentsViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    # permission_classes = (AuthorOrReadOnly,)

    def get_queryset(self):
        url_review_id = self.kwargs.get("url_review_id")
        return Comments.objects.filter(review_id=url_review_id)

    def perform_create(self, serializer):
        author = self.request.user
        comment = get_object_or_404(
            Comments,
            id=self.kwargs.get("url_review_id")
        )
        serializer.save(author=author, review_id=comment)


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
