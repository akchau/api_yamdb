from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import UserViewSet, UserRegistrationViewSet

app_name = "users"

router = DefaultRouter()
router.register(r'signup', UserRegistrationViewSet)
router.register('',  UserViewSet)

urlpatterns = [
    path('', include(router.urls))
]
