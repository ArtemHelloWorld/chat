import datetime

import django.conf
import django.contrib.auth.models
import django.core.mail
import django.core.signing
import django.urls

import users.models

MESSAGE_REGISTRATION = 'Для завершения регистрации перейдите по ссылке:\n{}'
MESSAGE_REACTIVATION = (
    'Вы превысили максимальное количество попыток входа в аккаунт.\n'
    'Для активации перейдите по ссылке:\n{}'
)


def send_email_with_activation_link(request, user, reactivation=False):
    if reactivation:
        message = MESSAGE_REACTIVATION.format(
            request.build_absolute_uri(
                generate_activation_link(user, reactivation=True)
            )
        )
    else:
        message = MESSAGE_REGISTRATION.format(
            request.build_absolute_uri(generate_activation_link(user))
        )

    django.core.mail.send_mail(
        subject='Subject',
        message=message,
        from_email=django.conf.settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
    )


def generate_activation_link(user, reactivation=False):
    signer = django.core.signing.TimestampSigner()
    if reactivation:
        viewname = 'users:reactivation'
    else:
        viewname = 'users:signup_activate'

    activation_code = signer.sign(user.username)

    link = django.urls.reverse(
        viewname, kwargs={'activation_code': activation_code}
    )
    return link


def validate_activation_link(value, **kwargs):
    signer = django.core.signing.TimestampSigner()
    max_age = datetime.timedelta(**kwargs)

    try:
        username = signer.unsign(value, max_age=max_age)
    except Exception:
        return None

    user = users.models.User.objects.get(username=username)
    return user


def generate_normalize_email(email):
    if '@' in email:
        email = email.lower()
        name, domain = email.split('@')

        name = name.split('+')[0]

        if domain == 'ya.ru':
            domain = 'yandex.ru'

        if domain == 'gmail.com':
            name = name.replace('.', '')

        if domain == 'yandex.ru':
            name = name.replace('.', '-')

        return f'{name}@{domain}'

    else:
        return email
