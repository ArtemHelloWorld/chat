# Generated by Django 3.2.16 on 2023-09-01 18:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0023_remove_message_file'),
    ]

    operations = [
        migrations.CreateModel(
            name='MessageFile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(null=True, upload_to='', verbose_name='фотография')),
            ],
        ),
        migrations.AddField(
            model_name='message',
            name='file',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='chat.messagefile'),
        ),
    ]
