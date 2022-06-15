from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import UserViewSet, UserRegistrationViewSet, UserMeApi

app_name = "users"

router = DefaultRouter()
router.register(r"signup", UserRegistrationViewSet)
router.register(r"token", UserRegistrationViewSet)


urlpatterns = [
    path("", include(router.urls)),
]
