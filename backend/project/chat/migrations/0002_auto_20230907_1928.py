# Generated by Django 3.2.16 on 2023-09-07 16:28

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('chat', '0001_initial_squashed_0025_alter_messagefile_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='chat',
            name='user1',
        ),
        migrations.RemoveField(
            model_name='chat',
            name='user2',
        ),
        migrations.AddField(
            model_name='chat',
            name='users',
            field=models.ManyToManyField(
                related_name='users', to=settings.AUTH_USER_MODEL
            ),
        ),
    ]
