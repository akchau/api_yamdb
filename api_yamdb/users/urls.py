"""urls приложения users."""
from rest_framework.routers import DefaultRouter
from django.urls import path, include

from .views import UserViewSet, UserMeView, UserActivationView

app_name = "users"

router = DefaultRouter()
router.register(r"users", UserViewSet)


urlpatterns = [
    path("v1/auth/signup/", UserActivationView.as_view()),
    path("v1/users/me/", UserMeView.as_view()),
    path("v1/", include(router.urls)),
]
