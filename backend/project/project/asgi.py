import os

from channels.security.websocket import AllowedHostsOriginValidator
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter

import chat.routing
from chat.middleware import QueryAuthMiddleware, JwtAuthMiddleware

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')

application = ProtocolTypeRouter(
    {
        'http': get_asgi_application(),
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
