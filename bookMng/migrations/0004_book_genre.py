# Generated by Django 5.1.5 on 2025-04-22 23:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookMng', '0003_book_favorites'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='genre',
            field=models.CharField(choices=[('Fiction', 'Fiction'), ('Nonfiction', 'Nonfiction'), ('Mystery', 'Mystery'), ('Fantasy', 'Fantasy'), ('Other', 'Other')], default='Other', max_length=50),
        ),
    ]
