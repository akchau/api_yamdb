"""Роутер приложения users."""
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import RegisterView, TokenView, UserMeView, UserViewSet

app_name = "users"

router = DefaultRouter()
router.register(r"users", UserViewSet)

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
