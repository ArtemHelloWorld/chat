from django.db import models
import users.models
import core.models


class Message(models.Model):
    chat = models.ForeignKey('Chat', on_delete=models.CASCADE, related_name='chat')
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


class Chat(models.Model):
    user1 = models.ForeignKey(users.models.User, on_delete=models.CASCADE, related_name='user1')
    user2 = models.ForeignKey(users.models.User, on_delete=models.CASCADE, related_name='user2')
    last_message = models.ForeignKey(Message, on_delete=models.SET_NULL, null=True, related_name='last_message', verbose_name='последнее сообщение')
    status = models.JSONField(default=dict, verbose_name='статус, например, что пользователь печатает')
    created_timestamp = core.models.TimestampField(auto_now=True, verbose_name='время создания чата')

    def __str__(self):
        return f'Чат {self.pk}'

    class Meta:
        verbose_name = 'чат'
        verbose_name_plural = 'чаты'


