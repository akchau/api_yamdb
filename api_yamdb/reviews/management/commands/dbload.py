import csv
from django.conf import settings
from django.core.management.base import BaseCommand
from reviews.models import (
    Titles,
    Genres,
    GenreTitle,
    User,
    Comments,
    Review,
    Categories
)


STATIC_PATH = f'{settings.BASE_DIR}/static/data/'


class Command(BaseCommand):
    help = 'Загрузка данных, получаемых вместе с проектом'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        mod_dic = {
            'users.csv': User,
            'category.csv': Categories,
            'genre.csv': Genres,
            'titles.csv': Titles,
            'genre_title.csv': GenreTitle,
            'review.csv': Review,
            'comments.csv': Comments,
        }
        for file, model in mod_dic.items():
            database = model
            with open(f'{STATIC_PATH}/{file}') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if "titles.csv" in file:
                        cat = Categories.objects.get(id=row.pop('category'))
                        database.objects.create(category=cat, **row)
                    elif 'genre_title.csv' in file:
                        t_id = Titles.objects.get(id=row['title_id'])
                        g_id = Genres.objects.get(id=row['genre_id'])
                        database.objects.create(title_id=t_id, genre_id=g_id)
                    elif 'review.csv' in file:
                        t_id = Titles.objects.get(id=row.pop('title_id'))
                        usr = User.objects.get(id=row.pop('author'))
                        database.objects.create(
                            title_id=t_id,
                            author=usr,
                            **row
                        )
                    elif 'comments.csv' in file:
                        r_id = Review.objects.get(id=row.pop('review_id'))
                        usr = User.objects.get(id=row.pop('author'))
                        database.objects.create(
                            review_id=r_id,
                            author=usr,
                            **row)
                    else:
                        database.objects.create(**row)
