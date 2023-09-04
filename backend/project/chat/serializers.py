import rest_framework.serializers
import rest_framework

from users.serializers import ProfileSerializer

import chat.models


class MessageSerializer(rest_framework.serializers.ModelSerializer):
    class Meta:
        model = chat.models.Message
        fields = ['id', 'sender', 'text', 'is_read', 'sending_timestamp']


class ChatSerializer(rest_framework.serializers.ModelSerializer):
    companion = rest_framework.serializers.SerializerMethodField(allow_null=True)
    last_message_info = rest_framework.serializers.SerializerMethodField(allow_null=True)

    class Meta:
        model = chat.models.Chat
        fields = ['id', 'user1', 'user2', 'last_message', 'status', 'created_timestamp', 'companion', 'last_message_info']

    def get_companion(self, obj):
        sender = self.context['request'].user
        if obj.user1 == sender:
            companion_serializer = ProfileSerializer(obj.user2)
        else:
            companion_serializer = ProfileSerializer(obj.user1)
        return companion_serializer.data

    def get_last_message_info(self, obj):
        if obj.last_message:
            return MessageSerializer(obj.last_message).data
        return None


class MessageFileSerializer(rest_framework.serializers.ModelSerializer):
    class Meta:
        model = chat.models.MessageFile
        fields = '__all__'
