import django.contrib.admin

import chat.models


@django.contrib.admin.register(chat.models.Chat)
class ChatAdmin(django.contrib.admin.ModelAdmin):
    list_display = (
        chat.models.Chat.id.field.name,
        chat.models.Chat.last_message.field.name,
        chat.models.Chat.status.field.name,
        chat.models.Chat.created_timestamp.field.name,
    )


@django.contrib.admin.register(chat.models.Message)
class MessageAdmin(django.contrib.admin.ModelAdmin):
    list_display = (
        chat.models.Message.id.field.name,
        chat.models.Message.text.field.name,
        chat.models.Message.is_read.field.name,
        chat.models.Message.sending_timestamp.field.name,
    )
