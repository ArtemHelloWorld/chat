import rest_framework.serializers
import rest_framework

import chat.models


class ChatSerializer(rest_framework.serializers.ModelSerializer):
    companion = rest_framework.serializers.JSONField(allow_null=True)

    class Meta:
        model = chat.models.Chat
        fields = ['id', 'user1', 'user2', 'last_message', 'status', 'companion']


class MessageSerializer(rest_framework.serializers.ModelSerializer):
    class Meta:
        model = chat.models.Message
        fields = ['id', 'sender', 'text', 'is_read', 'sending_timestamp']
