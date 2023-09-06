import os

import channels.routing
import channels.security.websocket
import django.core.asgi
import django.urls
import django_eventstream

import chat.middleware
import chat.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')

application = channels.routing.ProtocolTypeRouter(
    {
        'http': channels.routing.URLRouter(
            [
                django.urls.path(
                    'api/v1/chat/notifications/<user_id>/<token>/events/',
                    chat.middleware.JwtAuthMiddleware(
                        channels.routing.URLRouter(
                            django_eventstream.routing.urlpatterns
                        )
                    ),
                    {'format-channels': ['notifications-{user_id}']},
                ),
                django.urls.re_path(
                    r'', django.core.asgi.get_asgi_application()
                ),
            ]
        ),
        'websocket': channels.security.websocket.AllowedHostsOriginValidator(
            chat.middleware.JwtAuthMiddleware(
                chat.middleware.QueryAuthMiddleware(
                    channels.routing.URLRouter(
                        chat.routing.websocket_urlpatterns
                    )
                )
            )
        ),
    }
)
