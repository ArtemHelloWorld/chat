import django.urls

import chat.consumers

websocket_urlpatterns = [
    django.urls.path(
        'ws/socket-server/chat/<str:token>/<int:chat_pk>/',
        chat.consumers.ChatConsumer.as_asgi(),
    )
]
