# Generated by Django 2.2.16 on 2022-06-20 18:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0004_auto_20220620_2310'),
    ]

    operations = [
        migrations.AlterField(
            model_name='titles',
            name='genre',
            field=models.ManyToManyField(blank=True, related_name='titles', through='reviews.GenreTitle', to='reviews.Genres', verbose_name='Жанр'),
        ),
    ]
