






from django.db import models
import users.models
import core.models


class Chat(models.Model):
    last_message = models.ForeignKey('Message', on_delete=models.SET_NULL, null=True, related_name='last_message',
                                     verbose_name='последнее сообщение')
    status = models.JSONField(default=dict, verbose_name='статус, например, что пользователь печатает')
    created_timestamp = core.models.TimestampField(auto_now=True, verbose_name='время создания чата')

    def __str__(self):
        return f'Чат {self.pk}'

    class Meta:
        verbose_name = 'чат'
        verbose_name_plural = 'чаты'


class ChatMember(models.Model):
    user = models.ForeignKey(users.models.User, on_delete=models.CASCADE, related_name='user')
    conversation = models.OneToOneField('Chat', on_delete=models.CASCADE, related_name='conversation')


    # todo: def save() проверка что еще не два участника чата
    def __str__(self):
        return f'Участник чата {self.pk}'

    class Meta:
        verbose_name = 'участник чата'
        verbose_name_plural = 'участники чатов'


class ChatConversation(models.Model):
    chat = models.OneToOneField('Chat', on_delete=models.CASCADE, related_name='chat')

    def __str__(self):
        return f'Беседа {self.pk}'

    class Meta:
        verbose_name = 'беседа'
        verbose_name_plural = 'беседы'


class Message(models.Model):
    conversation = models.ForeignKey('Conversation', on_delete=models.CASCADE, related_name='conversation')
    sender = models.ForeignKey(users.models.User, on_delete=models.CASCADE, related_name='sent_messages')
    text = models.TextField(verbose_name='текст сообщения')
    file = models.ForeignKey('MessageFile', null=True, on_delete=models.SET_NULL)
    is_read = models.BooleanField(default=False)
    sending_timestamp = core.models.TimestampField(auto_now=True, verbose_name='время отправки сообщения')

    def __str__(self):
        return f'Сообщение {self.pk}'

    class Meta:
        verbose_name = 'сообщение'
        verbose_name_plural = 'сообщения'
        ordering = ['sending_timestamp']


class MessageFile(models.Model):
    image = models.ImageField(upload_to='chat_images/%Y/%m/%d', null=True, verbose_name='фотография')

    def __str__(self):
        return f'Файл сообщения {self.pk}'

    class Meta:
        verbose_name = 'файл сообщения'
        verbose_name_plural = 'файлы сообщений'




import django.db.models

import core.models
import users.models


class Message(django.db.models.Model):
    chat = django.db.models.ForeignKey(
        'Chat', on_delete=django.db.models.CASCADE, related_name='chat'
    )
    sender = django.db.models.ForeignKey(
        users.models.User,
        on_delete=django.db.models.CASCADE,
        related_name='sent_messages',
    )
    text = django.db.models.TextField(verbose_name='текст сообщения')
    file = django.db.models.ForeignKey(
        'MessageFile', null=True, on_delete=django.db.models.SET_NULL
    )
    is_read = django.db.models.BooleanField(default=False)
    sending_timestamp = core.models.TimestampField(
        auto_now=True, verbose_name='время отправки сообщения'
    )

    def __str__(self):
        return f'Сообщение {self.pk}'

    class Meta:
        verbose_name = 'сообщение'
        verbose_name_plural = 'сообщения'
        ordering = ['sending_timestamp']


class MessageFile(django.db.models.Model):
    image = django.db.models.ImageField(
        upload_to='chat_images/%Y/%m/%d', null=True, verbose_name='фотография'
    )


class Chat(django.db.models.Model):
    user1 = django.db.models.ForeignKey(
        users.models.User,
        on_delete=django.db.models.CASCADE,
        related_name='user1',
    )
    user2 = django.db.models.ForeignKey(
        users.models.User,
        on_delete=django.db.models.CASCADE,
        related_name='user2',
    )
    last_message = django.db.models.ForeignKey(
        Message,
        on_delete=django.db.models.SET_NULL,
        null=True,
        related_name='last_message',
        verbose_name='последнее сообщение',
    )
    status = django.db.models.JSONField(
        default=dict,
        verbose_name='статус, например, что пользователь печатает',
    )
    created_timestamp = core.models.TimestampField(
        auto_now=True, verbose_name='время создания чата'
    )

    def __str__(self):
        return f'Чат {self.pk}'

    class Meta:
        verbose_name = 'чат'
        verbose_name_plural = 'чаты'
