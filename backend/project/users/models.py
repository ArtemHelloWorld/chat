import django.contrib.auth.models
import django.db.models

import core.services


class User(django.contrib.auth.models.AbstractUser):
    default_image_path = 'profile_images/default.png'

    bio = django.db.models.TextField(
        verbose_name='о себе', null=True, blank=True
    )
    profile_image = django.db.models.ImageField(
        verbose_name='фотография',
        upload_to='profile_images/%Y/%m/%d',
        default=default_image_path,
    )

    def save(self, *args, **kwargs):
        super(User, self).save(*args, **kwargs)
        profile_image = self.profile_image
        # обрезаем фото под квадрат
        if profile_image and profile_image != self.default_image_path:
            rectangle_image = core.services.image_to_rectangle(
                image_path=profile_image.path
            )
            rectangle_image.save(profile_image.path)

    def __str__(self):
        return f'Пользователь {self.pk}'

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ['-is_staff', '-date_joined', 'username']
