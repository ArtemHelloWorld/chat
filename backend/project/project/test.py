import django.contrib.auth.models
import django.forms.models
import django.shortcuts
import django.test
import django.urls


@django.test.override_settings(RATE_LIMIT_MIDDLEWARE=False)
class MyMiddlewareTestCase(django.test.TestCase):
    def setUp(self):
        self.client = django.test.Client()

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

    @django.test.override_settings(RATE_LIMIT_MIDDLEWARE=True)
    @django.test.override_settings(REQUESTS_PER_SECOND=2)
    def test_rate_limit_middleware(self):
        response = self.client.get(django.shortcuts.reverse('users:login'))
        self.assertEqual(response.status_code, 200)

        response = self.client.get(django.shortcuts.reverse('users:login'))
        self.assertEqual(response.status_code, 429)
