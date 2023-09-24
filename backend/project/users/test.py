import django.contrib.auth.models
import django.forms.models
import django.shortcuts
import django.test
import django.urls
import parameterized
import rest_framework.status
import rest_framework.test

import users.models


@django.test.override_settings(RATE_LIMIT_MIDDLEWARE=False)
class BaseUserAPITestCase(rest_framework.test.APITestCase):
    def setUp(self):
        self.me = users.models.User.objects.create_user('me', 'TestPassword1')
        self.client.force_authenticate(self.me)

        self.friend = users.models.User.objects.create_user(
            'friend', 'TestPassword1'
        )


class UserCreateAPITestCase(BaseUserAPITestCase):
    @parameterized.parameterized.expand(
        [
            (
                'no username, password',
                '',
                '',
                rest_framework.status.HTTP_400_BAD_REQUEST,
            ),
            (
                'no username',
                '',
                'TestPassword1',
                rest_framework.status.HTTP_400_BAD_REQUEST,
            ),
            (
                'no password',
                'username',
                '',
                rest_framework.status.HTTP_400_BAD_REQUEST,
            ),
            (
                'short(1) password',
                'username',
                't',
                rest_framework.status.HTTP_400_BAD_REQUEST,
            ),
            (
                'short(7) password',
                'username',
                'TestPa1',
                rest_framework.status.HTTP_400_BAD_REQUEST,
            ),
            (
                'numeric password',
                'username',
                '123456789101112',
                rest_framework.status.HTTP_400_BAD_REQUEST,
            ),
            (
                'hard password',
                'username',
                'TestPassword1',
                rest_framework.status.HTTP_200_OK,
            ),
        ]
    )
    def test_user_create(self, test_name, username, password, expected_status):
        user = {'username': username, 'password': password}
        url = django.urls.reverse('user-create')

        response = self.client.post(url, user)
        self.assertEqual(
            response.status_code, expected_status, f'Test {test_name} failed'
        )


class UserSearchTestCase(BaseUserAPITestCase):
    @parameterized.parameterized.expand(
        [
            ('suitable for no username', 'random text', 0),
            ('suitable for no username `me`', 'me1', 0),
            ('suitable for username `me`', 'me', 1),
            ('suitable for username `me`', 'm', 1),
            ('suitable for username `friend`', 'friend', 1),
            ('suitable for username `friend`', 'frien', 1),
            ('suitable for username `friend`', 'rien', 1),
            ('suitable for username `friend`', 'ien', 1),
            ('suitable for username `friend` and `me`', 'e', 2),
        ]
    )
    def test_user_search(
        self, test_name, username_filter, suitable_users_count
    ):
        url = django.urls.reverse(
            'user-search-list', kwargs={'username_filter': username_filter}
        )
        response = self.client.get(url)
        self.assertEqual(
            len(response.data),
            suitable_users_count,
            f'Test {test_name} failed',
        )


class ProfileReadUpdateTestCase(BaseUserAPITestCase):
    def test_profile_read_myself(self):
        user_id = self.me.id
        url = django.urls.reverse(
            'profile-read-update', kwargs={'user_id': user_id}
        )

        response = self.client.get(url)
        self.assertEqual(
            response.status_code, rest_framework.status.HTTP_200_OK
        )

    def test_profile_read_friend(self):
        user_id = self.friend.id
        url = django.urls.reverse(
            'profile-read-update', kwargs={'user_id': user_id}
        )

        response = self.client.get(url)
        self.assertEqual(
            response.status_code, rest_framework.status.HTTP_200_OK
        )

    def test_profile_update_myself(self):
        user_id = self.me.id
        new_user_data = {'username': f'{self.me.username}_new'}
        url = django.urls.reverse(
            'profile-read-update', kwargs={'user_id': user_id}
        )

        response = self.client.put(url, new_user_data)
        self.assertEqual(
            response.status_code, rest_framework.status.HTTP_200_OK
        )

    def test_profile_update_friend(self):
        user_id = self.friend.id
        new_user_data = {'username': f'{self.friend.username}_new'}
        url = django.urls.reverse(
            'profile-read-update', kwargs={'user_id': user_id}
        )

        response = self.client.put(url, new_user_data)
        self.assertEqual(
            response.status_code, rest_framework.status.HTTP_403_FORBIDDEN
        )
