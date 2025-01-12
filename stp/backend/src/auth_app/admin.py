from django.contrib import admin
from django.utils.html import format_html

from .models import UserSessions


class UserSessionsAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "ipv4",
        "user_agent",
        "created_at",
        "updated_at",
    )
    search_fields = ("user__email", "ipv4", "user_agent", "refresh_token")
    list_filter = ("created_at", "updated_at", "user__email")
    readonly_fields = (
        "user",
        "ipv4",
        "user_agent",
        "refresh_token_hidden",
        "created_at",
        "updated_at",
    )
    fieldsets = (
        (None, {"fields": ("user", "refresh_token_hidden", "ipv4", "user_agent")}),
        ("Timestamps", {"fields": ("created_at", "updated_at")}),
    )
    actions = ["delete_selected_sessions"]

    def refresh_token_hidden(self, obj):
        return format_html(
            '<span style="display: inline-block; overflow: hidden; '
            'text-overflow: ellipsis; background-color: gray; color: gray;" '
            "onmouseover=\"this.style.color='white';\" "
            'onmouseout="this.style.color=\'gray\';" title="{}">{}</span>',
            obj.refresh_token,
            obj.refresh_token,
        )

    refresh_token_hidden.short_description = "Refresh Token"

    def delete_selected_sessions(self, request, queryset):
        queryset.delete()

    delete_selected_sessions.short_description = "Delete selected sessions"


admin.site.register(UserSessions, UserSessionsAdmin)
