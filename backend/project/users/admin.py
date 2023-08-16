import django.contrib.admin

import users.models


@django.contrib.admin.register(users.models.User)
class UserAdmin(django.contrib.admin.ModelAdmin):
    list_display = (
        users.models.User.username.field.name,
        users.models.User.email.field.name,
        users.models.User.first_name.field.name,
        users.models.User.last_name.field.name,
        users.models.User.date_joined.field.name,
        'is_active',  # users.models.User.is_active.field.name,
        users.models.User.is_staff.field.name,
    )
    list_display_links = (
        users.models.User.username.field.name,
        users.models.User.email.field.name,
    )
