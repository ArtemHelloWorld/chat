from django.urls import path

import chat.views_api

urlpatterns = [
    path('chat/user/<str:username>/', chat.views_api.ChatUserInfoView.as_view(), name='chat-with-user'),
    path('chat/user/<str:username>/messages/', chat.views_api.ChatUserMessagesInfoView.as_view(), name='chat-messages-with-user'),
    path('chat/<str:chat_id>/messages/', chat.views_api.ChatMessagesInfoView.as_view(), name='chat-messages'),
]
