# Generated by Django 4.2.4 on 2023-08-03 15:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0003_alter_chat_messages'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userchat',
            name='time_created',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
