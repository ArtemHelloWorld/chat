import rest_framework.serializers
import chat.models


class ChatSerializer(rest_framework.serializers.ModelSerializer):
    class Meta:
        model = chat.models.Chat
        fields = ['id', 'user1', 'user2']


class MessageSerializer(rest_framework.serializers.ModelSerializer):
    class Meta:
        model = chat.models.Message
        fields = ['id', 'sender', 'text', 'is_read', 'sending_timestamp']
