# Generated by Django 3.2.16 on 2023-08-21 14:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_auto_20230821_1835'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='last_online',
        ),
    ]