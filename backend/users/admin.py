from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html

from .models import CustomUser, Location, Match


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
        'avatar_tag',
        'id'
    )
    list_filter = (
        'username',
        'sex'
    )
    fieldsets = UserAdmin.fieldsets + (
            (None, {'fields': ('sex', 'avatar')}),
    )


@admin.register(Match)
class MatchAdmin(admin.ModelAdmin):
    list_display = (
        'liking_client',
        'liked_client'
    )


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = (
        'client',
        'latitude',
        'longitude'
    )
