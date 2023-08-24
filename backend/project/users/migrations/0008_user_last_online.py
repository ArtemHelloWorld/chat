# Generated by Django 3.2.16 on 2023-08-21 14:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_remove_user_last_online'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='last_online',
            field=models.PositiveBigIntegerField(default=0, verbose_name='последний раз онлайн'),
        ),
    ]