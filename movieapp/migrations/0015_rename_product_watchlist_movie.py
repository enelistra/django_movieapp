# Generated by Django 5.0.3 on 2024-04-01 05:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('movieapp', '0014_rename_cart_watchlist'),
    ]

    operations = [
        migrations.RenameField(
            model_name='watchlist',
            old_name='product',
            new_name='movie',
        ),
    ]
