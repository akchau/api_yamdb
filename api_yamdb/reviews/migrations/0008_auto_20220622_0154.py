# Generated by Django 2.2.16 on 2022-06-21 20:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0007_auto_20220622_0101'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='titles',
            options={'ordering': ('id',), 'verbose_name': 'Произведение', 'verbose_name_plural': 'Произведения'},
        ),
        migrations.RemoveConstraint(
            model_name='titles',
            name='title_category',
        ),
    ]
