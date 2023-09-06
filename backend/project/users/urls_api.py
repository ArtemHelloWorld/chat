import django.urls

import users.views_api

app_name = 'users'

urlpatterns = [
    django.urls.path(
        'user/search/<str:username_filter>/',
        users.views_api.UserSearchListApiView.as_view(),
        name='user-search',
    ),
    django.urls.path(
        'user/<int:user_id>/',
        users.views_api.UserRetrieveUpdateAPIView.as_view(),
        name='profile-read-update',
    ),
    django.urls.path(
        'user/register/',
        users.views_api.UserRegisterView.as_view(),
        name='user-create',
    ),
]
