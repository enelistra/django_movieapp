# Generated by Django 5.0.3 on 2024-03-28 04:46

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movieapp', '0011_remove_reviews_user_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='reply',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.TextField()),
                ('username', models.CharField(max_length=150)),
                ('review', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='replies', to='movieapp.reviews')),
            ],
        ),
    ]
