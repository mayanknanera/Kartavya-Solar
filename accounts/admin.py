from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(BaseUserAdmin):

    list_display = (
        "email",
        "first_name",
        "last_name",
        "phone",
        "is_staff",
        "is_active",
        "date_joined",
    )

    list_filter = ("is_staff", "is_superuser", "is_active", "date_joined")

    search_fields = ("email", "first_name", "last_name", "phone")

    ordering = ("-date_joined",)

    readonly_fields = ("date_joined", "last_login")

    # Organize fields into sections
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Personal Info", {"fields": ("first_name", "last_name", "phone")}),
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
        ("Important Dates", {"fields": ("last_login", "date_joined")}),
    )

    # Fields when creating new user
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "first_name",
                    "last_name",
                    "phone",
                    "password1",
                    "password2",
                    "is_staff",
                    "is_active",
                ),
            },
        ),
    )
