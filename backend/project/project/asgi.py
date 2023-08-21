import os

import django_eventstream
from channels.auth import AuthMiddlewareStack
from channels.security.websocket import AllowedHostsOriginValidator
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter

import chat.routing
from chat.middleware import QueryAuthMiddleware, JwtAuthMiddleware
from django.urls import path, re_path

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')

application = ProtocolTypeRouter(
    {
        'http': URLRouter([
            path('api/v1/chat/notifications/<user_id>/<token>/events/', JwtAuthMiddleware(
                URLRouter(django_eventstream.routing.urlpatterns)
            ), {'format-channels': ['notifications-{user_id}']}),
            re_path(r'', get_asgi_application()),
        ]),
        'websocket': AllowedHostsOriginValidator(
            JwtAuthMiddleware(
                QueryAuthMiddleware(
                    URLRouter(
                        chat.routing.websocket_urlpatterns
                    )
                )
            )
        )
    }
)
