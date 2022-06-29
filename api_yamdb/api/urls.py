"""Эндпойнты приложения 'api'."""
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from users.views import RegisterView, TokenView, UserMeView, UserViewSet

from .views import (CategoriesViewSet, CommentsViewSet, GenresViewSet,
                    ReviewViewSet, TitleViewSet)

app_name = "api"

router = DefaultRouter()
router.register(r"users/me", UserViewSet, basename='me')
router.register(r"users", UserViewSet, basename='users')
router.register(r'categories', CategoriesViewSet, basename='categories')
router.register(r'genres', GenresViewSet, basename='genres')
router.register(r'titles', TitleViewSet, basename='titles')
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
    # path("v1/users/me/", UserMeView.as_view()),
    path("v1/", include(router.urls)),
]
