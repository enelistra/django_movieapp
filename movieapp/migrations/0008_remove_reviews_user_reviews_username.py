# Generated by Django 5.0.3 on 2024-03-27 13:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movieapp', '0007_rename_my_movie_reviews_movie_alter_reviews_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='reviews',
            name='user',
        ),
        migrations.AddField(
            model_name='reviews',
            name='username',
            field=models.CharField(default=1, max_length=150),
            preserve_default=False,
        ),
    ]