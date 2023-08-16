import django.conf
import django.contrib.auth.backends
import django.contrib.auth.hashers
import django.contrib.auth.models
import django.forms

import users.models
import users.services


class AuthByEmailOrUsernameBackend(django.contrib.auth.backends.BaseBackend):
    def authenticate(self, request, username=None, password=None):
        if '@' in username:
            query_filter = {
                'email': users.services.generate_normalize_email(username)
            }

        else:
            query_filter = {'username': username}

        try:
            user = users.models.User.objects.get(**query_filter)
        except users.models.User.DoesNotExist:
            return None

        if user.check_password(password):
            return user
        else:
            count = request.session.get('load_count', 0) + 1
            request.session['load_count'] = count

            if count == django.conf.settings.MAX_FAILED_LOGIN_ATTEMPTS:
                request.session['load_count'] = 0

                user.is_active = False
                user.save()

                users.services.send_email_with_activation_link(
                    request, user, reactivation=True
                )

                raise django.forms.ValidationError(
                    'Вы превысили количество попыток войти. '
                    'На вашу почту отправлено письмо '
                    'cо ссылкой для восстановления аккаунта'
                )
            return None

    def get_user(self, user_id):
        try:
            return users.models.User.objects.get(pk=user_id)
        except users.models.User.DoesNotExist:
            return None
