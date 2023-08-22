import django.core.exceptions
import django.db.models
import django.shortcuts
import rest_framework.generics
import rest_framework.permissions
from django.db import models
from django.db.models import Q, Case, When, F, CharField, Value, JSONField
from django.db.models.functions import JSONObject

import chat.models
import chat.serializers
import users.models


class ChatAll(rest_framework.generics.ListAPIView):
    permission_classes = [rest_framework.permissions.IsAuthenticated]
    serializer_class = chat.serializers.ChatSerializer

    def get_queryset(self):
        sender = self.request.user
        # todo: вынести select related  в общий функциоал
        chat_list = chat.models.Chat.objects.filter(
            (django.db.models.Q(user1=sender) | django.db.models.Q(user2=sender))
        ).annotate(
            companion=Case(
                When(user1=sender, then=JSONObject(
                    id=F('user2__id'),
                    username=F('user2__username'),
                    email=F('user2__email'),
                    is_online=F('user2__is_online'),
                    last_online=F('user2__last_online'),
                )),
                When(user2=sender, then=JSONObject(
                    id=F('user1__id'),
                    username=F('user1__username'),
                    email=F('user1__email'),
                    is_online=F('user1__is_online'),
                    last_online=F('user1__last_online'),
                )),
                output_field=JSONField()
            )
        )
        return chat_list


class ChatUserInfoView(rest_framework.generics.RetrieveAPIView):
    permission_classes = [rest_framework.permissions.IsAuthenticated]
    serializer_class = chat.serializers.ChatSerializer

    def get_object(self):
        sender = self.request.user
        receiver = django.shortcuts.get_object_or_404(users.models.User, username=self.kwargs['username'])
        try:
            chat_obj = chat.models.Chat.objects.get(
                (django.db.models.Q(user1=sender, user2=receiver) | django.db.models.Q(user1=receiver, user2=sender))
            )

        except django.core.exceptions.ObjectDoesNotExist:
            chat_obj = chat.models.Chat.objects.create(
                user1=sender,
                user2=receiver,
            )
        chat_obj.companion = {
            'id': receiver.id,
            'username': receiver.username,
            'email': receiver.email,
            'is_online': receiver.is_online,
            'last_online': receiver.last_online,
        }

        return chat_obj


class ChatUserMessagesInfoView(rest_framework.generics.ListCreateAPIView):
    permission_classes = [rest_framework.permissions.IsAuthenticated]
    serializer_class = chat.serializers.MessageSerializer

    def get_queryset(self):
        sender = self.request.user
        receiver = django.shortcuts.get_object_or_404(users.models.User, username=self.kwargs['username'])
        try:
            chat_obj = chat.models.Chat.objects.get(
                (django.db.models.Q(user1=sender, user2=receiver) | django.db.models.Q(user1=receiver, user2=sender))
            )

        except django.core.exceptions.ObjectDoesNotExist:
            chat_obj = chat.models.Chat.objects.create(
                user1=sender,
                user2=receiver,
            )
        return chat.models.Message.objects.filter(chat=chat_obj)


class ChatMessagesInfoView(rest_framework.generics.ListCreateAPIView):
    permission_classes = [rest_framework.permissions.IsAuthenticated]
    serializer_class = chat.serializers.MessageSerializer

    def get_queryset(self):
        chat_obj = django.shortcuts.get_object_or_404(chat.models.Chat, id=self.kwargs['chat_id'])
        return chat.models.Message.objects.filter(chat=chat_obj)
