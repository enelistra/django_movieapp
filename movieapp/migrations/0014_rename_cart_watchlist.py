# Generated by Django 5.0.3 on 2024-04-01 05:37

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('movieapp', '0013_cart'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RenameModel(
            old_name='cart',
            new_name='watchlist',
        ),
    ]
