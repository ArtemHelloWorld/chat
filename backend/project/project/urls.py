import django.conf.urls.static
import django.contrib.admin
import django.urls
import rest_framework_simplejwt.views

import chat.views
import users.views

urlpatterns = [
    django.urls.path(
        'api/v1/token/',
        rest_framework_simplejwt.views.TokenObtainPairView.as_view(),
        name='token_obtain_pair',
    ),
    django.urls.path(
        'api/v1/token/refresh/',
        rest_framework_simplejwt.views.TokenRefreshView.as_view(),
        name='token_refresh',
    ),
    # todo: use token verify
    django.urls.path(
        'api/v1/token/verify/',
        rest_framework_simplejwt.views.TokenVerifyView.as_view(),
        name='token_verify',
    ),
    django.urls.path(
        'api/v1/user/signup/',
        users.views.UserCreateAPIView.as_view(),
        name='user-create',
    ),
    django.urls.path(
        'api/v1/user/search/<str:username_filter>/',
        users.views.UserSearchListApiView.as_view(),
        name='user-search-list',
    ),
    django.urls.path(
        'api/v1/profile/<int:user_id>/',
        users.views.ProfileRetrieveUpdateAPIView.as_view(),
        name='profile-read-update',
    ),
    django.urls.path(
        'api/v1/chat/all/',
        chat.views.ChatListAPIView.as_view(),
        name='chat-all-list',
    ),
    django.urls.path(
        'api/v1/chat/user/<str:username>/',
        chat.views.ChatUserRetrieveAPIView.as_view(),
        name='chat-user-read',
    ),
    django.urls.path(
        'api/v1/chat/<int:chat_id>/messages/',
        chat.views.ChatMessagesListCreateAPIView.as_view(),
        name='messages-list-create',
    ),
    django.urls.path(
        'api/v1/message/file/upload/',
        chat.views.MessageFileCreateAPIView.as_view(),
        name='message-file-create',
    ),
    django.urls.path('admin/', django.contrib.admin.site.urls),
    django.urls.path('api-auth/', django.urls.include('rest_framework.urls')),
]

urlpatterns += django.conf.urls.static.static(
    django.conf.settings.MEDIA_URL,
    document_root=django.conf.settings.MEDIA_ROOT,
)
