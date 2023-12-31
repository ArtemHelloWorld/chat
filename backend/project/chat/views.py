import django.core.exceptions
import django.db.models
import django.shortcuts
import rest_framework.generics
import rest_framework.permissions

import chat.models
import chat.serializers
import core.permissions
import users.models


def get_chat_or_create(user, companion):
    try:
        chat_obj = chat.models.Chat.objects.filter(users=user).get(
            users=companion
        )
    except django.core.exceptions.ObjectDoesNotExist:
        chat_obj = chat.models.Chat.objects.create()
        chat_obj.users.add(user, companion)
    except django.core.exceptions.MultipleObjectsReturned:
        print('MultipleObjectsReturned', 'chat.models.Chat', user, companion)
        chat_list = (
            chat.models.Chat.objects.filter(users=user)
            .filter(users=companion)
            .order_by('-created_timestamp')
        )
        return chat_list[0]

    return chat_obj


class ChatListAPIView(rest_framework.generics.ListAPIView):
    serializer_class = chat.serializers.ChatSerializer

    def get_queryset(self):
        sender = self.request.user
        chat_list = chat.models.Chat.objects.filter(
            django.db.models.Q(users=sender)
        )
        return chat_list


class ChatUserRetrieveAPIView(rest_framework.generics.RetrieveAPIView):
    serializer_class = chat.serializers.ChatSerializer

    def get_object(self):
        user = self.request.user
        companion = django.shortcuts.get_object_or_404(
            users.models.User, username=self.kwargs['username']
        )
        chat_obj = get_chat_or_create(user, companion)

        return chat_obj


class ChatMessagesListCreateAPIView(rest_framework.generics.ListCreateAPIView):
    permission_classes = [core.permissions.HaveMessagePermission]
    serializer_class = chat.serializers.MessageSerializer

    def get_queryset(self):
        chat_obj = django.shortcuts.get_object_or_404(
            chat.models.Chat, id=self.kwargs['chat_id']
        )
        return chat.models.Message.objects.filter(chat=chat_obj)


class MessageFileCreateAPIView(rest_framework.generics.CreateAPIView):
    serializer_class = chat.serializers.MessageFileSerializer
