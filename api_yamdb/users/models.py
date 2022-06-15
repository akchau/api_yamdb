from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    "Кастомный класс юзера"
    email = models.EmailField(blank=False)
    bio = models.TextField(
        "Биография",
        blank=True,
    )
    role = models.CharField(
        "Пользовательская роль",
        max_length=200,
        blank=True,
    )
