import django.contrib.auth.models
import django.forms.models
import django.shortcuts
import django.test
import django.urls
import rest_framework.test
import rest_framework.authtoken.models
from rest_framework import status


@django.test.override_settings(RATE_LIMIT_MIDDLEWARE=False)
class MyMiddlewareTestCase(rest_framework.test.APITestCase):
    def setUp(self):
        response = self.client.post(
            django.urls.reverse('users:user-create'),
            {
                'username': 'admin',
                'password': 123
            }
        )
        self.assertEqual(status.HTTP_200_OK, response.status_code)

        response = self.client.post(
            django.urls.reverse('token_obtain_pair'),
            {
                'username': 'admin',
                'password': '123'
            }
        )
        self.assertEqual(status.HTTP_200_OK, response.status_code)

        token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

    @django.test.override_settings(RATE_LIMIT_MIDDLEWARE=True)
    @django.test.override_settings(REQUESTS_PER_SECOND=2)
    def test_rate_limit_middleware(self):
        url = django.urls.reverse('users:profile-read-update', kwargs={'user_id': 1})

        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        response = self.client.get(url)
        self.assertEqual(response.status_code, 429)
