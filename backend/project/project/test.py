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
    @django.test.override_settings(RATE_LIMIT_MIDDLEWARE=True)
    @django.test.override_settings(REQUESTS_PER_SECOND=2)
    def test_rate_limit_middleware(self):
        user1 = {'username': 'admin1', 'password': 'TestPassword1'}
        user2 = {'username': 'admin2', 'password': 'TestPassword1'}
        url = django.urls.reverse('user-create')

        response = self.client.post(url, user1)
        self.assertEqual(
            response.status_code, rest_framework.status.HTTP_200_OK
        )

        response = self.client.post(url, user2)
        self.assertEqual(
            response.status_code,
            rest_framework.status.HTTP_429_TOO_MANY_REQUESTS,
        )
