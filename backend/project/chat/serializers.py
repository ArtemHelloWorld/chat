import rest_framework
import rest_framework.serializers

import chat.models
import users.serializers


class MessageSerializer(rest_framework.serializers.ModelSerializer):
    file = rest_framework.serializers.SerializerMethodField(allow_null=True)

    class Meta:
        model = chat.models.Message
        fields = [
            'id',
            'sender',
            'text',
            'is_read',
            'sending_timestamp',
            'file',
        ]

    def get_file(self, obj):
        if obj.file:
            return obj.file.image.url


class ChatSerializer(rest_framework.serializers.ModelSerializer):
    companion = rest_framework.serializers.SerializerMethodField(
        allow_null=True
    )
    last_message_info = rest_framework.serializers.SerializerMethodField(
        allow_null=True
    )

    class Meta:
        model = chat.models.Chat
        fields = [
            'id',
            'last_message',
            'status',
            'created_timestamp',
            'companion',
            'last_message_info',
        ]

    def get_companion(self, obj):
        sender = self.context['request'].user
        if sender in obj.users.all():
            print(obj.users.all())

            companion_serializer = users.serializers.ProfileSerializer(
                obj.users.all()[1]
            )
        else:
            companion_serializer = users.serializers.ProfileSerializer(
                obj.users.all()[0]
            )
        return companion_serializer.data

    def get_last_message_info(self, obj):
        if obj.last_message:
            return MessageSerializer(obj.last_message).data
        return None


class MessageFileSerializer(rest_framework.serializers.ModelSerializer):
    class Meta:
        model = chat.models.MessageFile
        fields = '__all__'
