# Generated by Django 3.2.16 on 2023-08-24 10:05

import core.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0015_alter_message_sending_timestamp'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='chat',
            name='time_created',
        ),
        migrations.AddField(
            model_name='chat',
            name='created_timestamp',
            field=core.models.TimestampField(blank=True, default=0, editable=False, verbose_name='время создания чата'),
            preserve_default=False,
        ),
    ]