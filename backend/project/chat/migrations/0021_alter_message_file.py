# Generated by Django 3.2.16 on 2023-09-01 15:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0020_message_file'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='file',
            field=models.ImageField(null=True, upload_to='', verbose_name='прикрепленный файл'),
        ),
    ]
