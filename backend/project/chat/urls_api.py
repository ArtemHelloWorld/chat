import django.urls

import chat.views_api

urlpatterns = [
    django.urls.path(
        'chat/all/', chat.views_api.ChatAll.as_view(), name='chat-all'
    ),
    django.urls.path(
        'chat/user/<str:username>/',
        chat.views_api.ChatUserInfoView.as_view(),
        name='chat-with-user',
    ),
    django.urls.path(
        'chat/<int:chat_id>/messages/',
        chat.views_api.ChatMessagesInfoView.as_view(),
        name='chat-messages',
    ),
    django.urls.path(
        'message/file/upload/',
        chat.views_api.MessageFileCreate.as_view(),
        name='message-file-upload',
    ),
]
