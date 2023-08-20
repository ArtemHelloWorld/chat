import django.contrib.admin
import chat.models


@django.contrib.admin.register(chat.models.Chat)
class ChatAdmin(django.contrib.admin.ModelAdmin):
    list_display = (
        chat.models.Chat.id.field.name,
        chat.models.Chat.user1.field.name,
        chat.models.Chat.user2.field.name,
        chat.models.Chat.time_created.field.name,
    )


@django.contrib.admin.register(chat.models.Message)
class MessageAdmin(django.contrib.admin.ModelAdmin):
    list_display = (
        chat.models.Message.id.field.name,
        chat.models.Message.text.field.name,
        chat.models.Message.is_read.field.name,
        chat.models.Message.sending_timestamp.field.name,
    )
