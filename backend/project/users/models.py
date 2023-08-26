import django.contrib.auth.models
import django.db.models

import core.services


class User(django.contrib.auth.models.AbstractUser):
    bio = django.db.models.TextField(verbose_name='о себе', null=True, blank=True)
    profile_image = django.db.models.ImageField(upload_to='profile_images/%Y/%m/%d', verbose_name='фотография', null=True, blank=True, default='profile_images/default.png')
    is_online = django.db.models.BooleanField(default=False, verbose_name='статус онлайна')
    last_online = django.db.models.PositiveBigIntegerField(default=0, verbose_name='последний раз онлайн')

    def save(self, *args, **kwargs):
        super(User, self).save(*args, **kwargs)
        # обрезаем фото под квадрат
        rectangle_image = core.services.image_to_rectangle(image_path=self.profile_image.path)
        rectangle_image.save(self.profile_image.path)

    def __str__(self):
        return f'Пользователь {self.pk}'

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ['-date_joined', 'username']
