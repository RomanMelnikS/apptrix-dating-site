from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html

from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    def avatar_tag(self, obj):
        if obj.avatar:
            return format_html(
                '<img src="{0}" style="max-width: 30%"/>',
                obj.avatar.url
            )

    avatar_tag.short_description = 'Аватар'

    list_display = (
        'username',
        'sex',
        'email',
        'first_name',
        'last_name',
        'avatar_tag'
    )
    list_filter = (
        'username',
        'sex'
    )

    fieldsets = UserAdmin.fieldsets + (
            (None, {'fields': ('sex', 'avatar')}),
    )
