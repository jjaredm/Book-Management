# Generated by Django 5.2 on 2025-05-01 07:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookMng', '0008_alter_book_picture_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='rating',
            field=models.PositiveSmallIntegerField(choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)], default=5),
        ),
    ]
