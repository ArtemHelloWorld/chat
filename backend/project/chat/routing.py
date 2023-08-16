from django.urls import path

import chat.consumers


websocket_urlpatterns = [
    path('ws/socket-server/chat/<str:token>/<int:chat_pk>/', chat.consumers.ChatConsumer.as_asgi())
]
