import django.db.models

import core.models
import users.models


class Message(django.db.models.Model):
    chat = django.db.models.ForeignKey(
        to='Chat',
        verbose_name='чат',
        on_delete=django.db.models.CASCADE,
        related_name='chat',
    )
    sender = django.db.models.ForeignKey(
        to=users.models.User,
        verbose_name='отправитель',
        on_delete=django.db.models.CASCADE,
        related_name='sender',
    )
    text = django.db.models.TextField(verbose_name='текст сообщения')
    file = django.db.models.ForeignKey(
        to='MessageFile',
        verbose_name='прикрепленный файл',
        null=True,
        on_delete=django.db.models.SET_NULL,
        related_name='file',
    )
    is_read = django.db.models.BooleanField(
        verbose_name='статус прочтения', default=False
    )
    sending_timestamp = core.models.TimestampField(
        verbose_name='время отправки сообщения', auto_now=True
    )

    def __str__(self):
        return f'Сообщение {self.pk}'

    class Meta:
        verbose_name = 'сообщение'
        verbose_name_plural = 'сообщения'
        ordering = ('sending_timestamp', 'pk')


class MessageFile(django.db.models.Model):
    image = django.db.models.ImageField(
        verbose_name='фотография',
        null=True,
        upload_to='chat_images/%Y/%m/%d',
    )


class Chat(django.db.models.Model):
    users = django.db.models.ManyToManyField(
        to=users.models.User, verbose_name='участники', related_name='users'
    )
    last_message = django.db.models.ForeignKey(
        to=Message,
        verbose_name='последнее сообщение',
        null=True,
        on_delete=django.db.models.SET_NULL,
        related_name='last_message',
    )
    status = django.db.models.JSONField(
        default=dict,
        verbose_name='статус активности пользователей',
    )
    created_timestamp = core.models.TimestampField(
        verbose_name='время создания чата', auto_now=True
    )

    def __str__(self):
        return f'Чат {self.pk}'

    class Meta:
        verbose_name = 'чат'
        verbose_name_plural = 'чаты'
        ordering = ('-created_timestamp', 'pk')
