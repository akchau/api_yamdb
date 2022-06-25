"""Эндпойнты приложения 'api'."""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (CommentsViewSet, ReviewViewSet,
                    CategoriesViewSet, GenresViewSet, TitlesViewSet)
from users.views import RegisterView, TokenView, UserMeView, UserViewSet


app_name = "api"

router = DefaultRouter()
router.register(r"users", UserViewSet)
router.register(r'categories', CategoriesViewSet, basename='categories')
router.register(r'genres', GenresViewSet, basename='genres')
router.register(r'titles', TitlesViewSet, basename='titles')
router.register(
    r'titles/(?P<url_title_id>\d+)/reviews',
    ReviewViewSet,
    basename='reviews'
)
router.register(
    r'titles/(?P<url_title_id>\d+)/reviews/(?P<url_review_id>\d+)/comments',
    CommentsViewSet,
    basename='comments'
)

urlpatterns = [
    path("v1/auth/signup/", RegisterView.as_view()),
    path(
        'v1/auth/token/',
        TokenView.as_view(),
        name='token_obtain_pair'
    ),
    path("v1/users/me/", UserMeView.as_view()),
    path("v1/", include(router.urls)),
]
