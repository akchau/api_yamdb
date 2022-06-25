"""urls приложения api."""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, UserMeView, CommentsViewSet, ReviewViewSet

app_name = "api"

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'users/me', UserMeView, basename='')
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
    path("v1/", include(router.urls)),
]