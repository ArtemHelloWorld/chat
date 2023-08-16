from channels.auth import AuthMiddlewareStack
from channels.db import database_sync_to_async
from channels.middleware import BaseMiddleware
from django.conf import settings
from django.contrib.auth.models import AnonymousUser
from django.db import close_old_connections
from django.http import HttpResponseNotFound
from django.shortcuts import get_object_or_404
from jwt import decode as jwt_decode
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.tokens import UntypedToken

import chat.models
import users.models


@database_sync_to_async
def get_chat(scope, chat_pk):
    user_chat = get_object_or_404(chat.models.Chat.objects.select_related('user1', 'user2'), pk=chat_pk)
    return user_chat


@database_sync_to_async
def get_user(validated_token):
    try:
        user = users.models.User.objects.get(id=validated_token['user_id'])
        return user
    except:
        return AnonymousUser()


class QueryAuthMiddleware:
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        self.scope = scope
        self.chat_pk = self.scope['path'].rstrip('/').split('/')[-1]

        self.chat_ = await get_chat(self.scope, self.chat_pk)
        await self.validate_user_permission_in_chat()
        await self.update_scope()

        return await self.app(self.scope, receive, send)

    async def validate_user_permission_in_chat(self):
        chat_participants = (self.chat_.user1, self.chat_.user2)
        if self.scope['user'] not in chat_participants:
            return HttpResponseNotFound

    async def update_scope(self):
        self.scope['chat_pk'] = self.chat_pk
        self.scope['chat_'] = self.chat_


class JwtAuthMiddleware(BaseMiddleware):
    def __init__(self, inner):
        self.inner = inner

    async def __call__(self, scope, receive, send):
        # close_old_connections()

        token = scope['path'].rstrip('/').split('/')[-2]

        try:
            UntypedToken(token)
        except (InvalidToken, TokenError) as e:
            return None
        else:
            decoded_data = jwt_decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            scope['user'] = await get_user(validated_token=decoded_data)
        return await super().__call__(scope, receive, send)


def JwtAuthMiddlewareStack(inner):
    return JwtAuthMiddleware(AuthMiddlewareStack(inner))
