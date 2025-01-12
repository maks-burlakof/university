from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import User


class UserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {"fields": ("username", "email", "password")}),
        (
            "Personal info",
            {
                "fields": (
                    "first_name",
                    "last_name",
                    "phone_number",
                    "profile_pic",
                    "description",
                    "site_url",
                    "gender",
                    "avatar_color",
                )
            },
        ),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "username",
                    "email",
                    "password1",
                    "password2",
                    "first_name",
                    "last_name",
                    "phone_number",
                ),
            },
        ),
    )
    readonly_fields = ("date_joined", "last_login")
    list_display = ("username", "email", "first_name", "last_name")
    search_fields = ("username", "email", "first_name", "last_name")
    ordering = ("username",)


admin.site.register(User, UserAdmin)
