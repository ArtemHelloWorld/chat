# Generated by Django 3.2.16 on 2023-08-24 13:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0017_alter_chat_last_message'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='chat',
            name='status',
        ),
    ]
