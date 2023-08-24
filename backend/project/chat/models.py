from django.db import models
import users.models
import core.models


class Message(models.Model):
    chat = models.ForeignKey('Chat', on_delete=models.CASCADE, related_name='chat')
    sender = models.ForeignKey(users.models.User, on_delete=models.CASCADE, related_name='sent_messages')
    text = models.TextField(verbose_name='текст сообщения')
    is_read = models.BooleanField(default=False)
    sending_timestamp = core.models.TimestampField(auto_now=True, verbose_name='время отправки сообщения')

    class Meta:
        verbose_name = 'сообщение'
        verbose_name_plural = 'сообщения'
        ordering = ['sending_timestamp']


class Chat(models.Model):
    user1 = models.ForeignKey(users.models.User, on_delete=models.CASCADE, related_name='user1')
    user2 = models.ForeignKey(users.models.User, on_delete=models.CASCADE, related_name='user2')
    last_message = models.ForeignKey(Message, on_delete=models.SET_NULL, null=True, related_name='last_message', verbose_name='последнее сообщение')
    status = models.TextField(null=True, default=None, verbose_name='статус, например, что пользователь печатает')
    created_timestamp = core.models.TimestampField(auto_now=True, verbose_name='время создания чата')

    def __str__(self):
        return f'Chat {self.pk}'

    class Meta:
        verbose_name = 'чат'
        verbose_name_plural = 'чаты'


