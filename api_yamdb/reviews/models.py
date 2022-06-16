from django.db import models
from users.models import User


class Categories(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField()


class Titles(models.Model):
    name = models.CharField(max_length=200)
    year = models.IntegerField('Год выхода')
    category = models.ForeignKey(
        Categories,
        on_delete=None,
        related_name='categories'
    )


class Genres(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField()


class GenereTitle(models.Model):
    title_id = models.ForeignKey(Titles, on_delete=None)
    genre_id = models.ForeignKey(Genres, on_delete=None)

    class Meta:

        unique_together = ('title_id', 'genre_id')


class Review(models.Model):
    title_id = models.ForeignKey(Titles, on_delete=None)
    text = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.IntegerField()
    pub_date = models.DateTimeField(
        'Дата публикации, отзыва',
        auto_now_add=True
    )


class Comments(models.Model):
    review_id = models.ForeignKey(Review, on_delete=models.CASCADE)
    text = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    pub_date = models.DateTimeField(
        'Дата публикации, комента',
        auto_now_add=True
    )
