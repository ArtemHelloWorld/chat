# Generated by Django 3.2.16 on 2023-08-19 15:47

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0009_alter_message_time_sending'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='message',
            options={'ordering': ['time_sending_timestamp'], 'verbose_name': 'сообщение', 'verbose_name_plural': 'сообщения'},
        ),
        migrations.RemoveField(
            model_name='message',
            name='time_sending',
        ),
        migrations.AddField(
            model_name='message',
            name='time_sending_timestamp',
            field=models.PositiveIntegerField(default=0, verbose_name='время отправки сообщения'),
            preserve_default=False,
        ),
    ]