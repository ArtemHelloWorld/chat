# Generated by Django 3.2.16 on 2023-08-21 14:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_user_last_online'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_online',
            field=models.BooleanField(default=False, verbose_name='статус онлайна'),
        ),
        migrations.AlterField(
            model_name='user',
            name='last_online',
            field=models.DateTimeField(verbose_name='последний раз онлайн'),
        ),
    ]