import channels.auth
import channels.db
import channels.middleware
import django.conf
import django.http
import django.shortcuts
import jwt
import rest_framework_simplejwt.exceptions
import rest_framework_simplejwt.tokens

import chat.models
import users.models


@channels.db.database_sync_to_async
def get_chat(chat_pk):
    user_chat = django.shortcuts.get_object_or_404(
        chat.models.Chat.objects.prefetch_related('users'), pk=chat_pk
    )
    return user_chat


@channels.db.database_sync_to_async
def get_user(validated_token):
    try:
        user = users.models.User.objects.get(id=validated_token['user_id'])
        return user
    except users.models.User.DoesNotExist:
        return None


class QueryAuthMiddleware:
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        self.scope = scope
        self.chat_pk = self.scope['path'].rstrip('/').split('/')[-1]

        self.chat_ = await get_chat(self.chat_pk)
        await self.validate_user_permission_in_chat()
        await self.update_scope()

        return await self.app(self.scope, receive, send)

    async def validate_user_permission_in_chat(self):
        if self.scope['user'] not in self.chat_.users.all():
            return django.http.HttpResponseNotFound

    async def update_scope(self):
        self.scope['chat_pk'] = self.chat_pk
        self.scope['chat_'] = self.chat_


class JwtAuthMiddleware(channels.middleware.BaseMiddleware):
    def __init__(self, inner):
        self.inner = inner

    async def __call__(self, scope, receive, send):
        # close_old_connections()

        token = scope['path'].rstrip('/').split('/')[-2]

        try:
            rest_framework_simplejwt.tokens.UntypedToken(token)
        except (
            rest_framework_simplejwt.exceptions.InvalidToken,
            rest_framework_simplejwt.exceptions.TokenError,
        ):
            return None
        else:
            decoded_data = jwt.decode(
                token, django.conf.settings.SECRET_KEY, algorithms=['HS256']
            )
            user = await get_user(validated_token=decoded_data)
            if not user:
                return django.http.HttpResponseNotFound
            scope['user'] = user
        return await super().__call__(scope, receive, send)


def JwtAuthMiddlewareStack(inner):
    return JwtAuthMiddleware(channels.auth.AuthMiddlewareStack(inner))
