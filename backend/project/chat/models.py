from django.db import models
import users.models


class Chat(models.Model):
    user1 = models.ForeignKey(users.models.User, on_delete=models.CASCADE, related_name='user1')
    user2 = models.ForeignKey(users.models.User, on_delete=models.CASCADE, related_name='user2')
    time_created = models.DateTimeField(auto_now=True, verbose_name='время создания чата')

    def __str__(self):
        return f'{self.pk}'

    class Meta:
        verbose_name = 'чат'
        verbose_name_plural = 'чаты'


class Message(models.Model):
    chat = models.ForeignKey('Chat', on_delete=models.CASCADE, related_name='chat')
    sender = models.ForeignKey(users.models.User, on_delete=models.CASCADE, related_name='sent_messages')
    # todo: изменить на message и pk на id
    text = models.TextField(verbose_name='текст сообщения')
    is_read = models.BooleanField(default=False)
    time_sending = models.DateTimeField(auto_now=True, verbose_name='время отправки сообщения')

    class Meta:
        verbose_name = 'сообщение'
        verbose_name_plural = 'сообщения'
        ordering = ['time_sending']

