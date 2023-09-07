import rest_framework.permissions


class HaveMessagePermission(rest_framework.permissions.BasePermission):
    message = 'Message is not allowed for you.'

    def has_object_permission(self, request, view, obj):
        return request.user in obj.chat.users
