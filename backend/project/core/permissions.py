import rest_framework.permissions


class HaveMessagePermission(rest_framework.permissions.BasePermission):
    message = 'Message is not allowed for you.'

    def has_object_permission(self, request, view, obj):
        obj_chat_users = (obj.chat.user1, obj.chat.user2)
        return request.user in obj_chat_users
