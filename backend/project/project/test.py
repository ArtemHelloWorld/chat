import django.contrib.auth.models
import django.forms.models
import django.shortcuts
import django.test
import django.urls
import rest_framework.authtoken.models
import rest_framework.status
import rest_framework.test


@django.test.override_settings(RATE_LIMIT_MIDDLEWARE=False)
class MyMiddlewareTestCase(rest_framework.test.APITestCase):
    def setUp(self):
        user_data = {'username': 'admin', 'password': 123}

        response = self.client.post(
            django.urls.reverse('users:user-create'), user_data
        )
        self.assertEqual(
            rest_framework.status.HTTP_200_OK, response.status_code
        )

        response = self.client.post(
            django.urls.reverse('token_obtain_pair'), user_data
        )
        self.assertEqual(
            rest_framework.status.HTTP_200_OK, response.status_code
        )

        token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

    @django.test.override_settings(RATE_LIMIT_MIDDLEWARE=True)
    @django.test.override_settings(REQUESTS_PER_SECOND=2)
    def test_rate_limit_middleware(self):
        url = django.urls.reverse(
            'users:profile-read-update', kwargs={'user_id': 1}
        )

        response = self.client.get(url)
        self.assertEqual(
            response.status_code, rest_framework.status.HTTP_200_OK
        )

        response = self.client.get(url)
        self.assertEqual(
            response.status_code,
            rest_framework.status.HTTP_429_TOO_MANY_REQUESTS,
        )
