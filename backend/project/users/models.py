import django.contrib.auth.models
import django.db.models
from django.utils import timezone


class User(django.contrib.auth.models.AbstractUser):
    bio = django.db.models.TextField(verbose_name='о себе', help_text='Напишите немного о себе', null=True, blank=True)
    image = django.db.models.ImageField(verbose_name='фотография', help_text='Выберете фотографию профиля', null=True, blank=True)
    is_online = django.db.models.BooleanField(default=False, verbose_name='статус онлайна')
    last_online = django.db.models.PositiveBigIntegerField(default=0, verbose_name='последний раз онлайн')

    def __str__(self):
        return f'Пользователь {self.pk}'

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ['-date_joined', 'username']
