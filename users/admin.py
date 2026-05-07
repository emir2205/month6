from django.contrib import admin
from users.models import CustomUser
from django.contrib.auth.admin import UserAdmin


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ("id", "email", "phone_number", "is_active")
    ordering = ("email",)
    search_fields = ("email", "phone_number")
    fieldsets = (
        (None, {"fields": ("email", "phone_number", "password")}),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        ("Important dates", {"fields": ("last_login",)}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "phone_number",
                    "usable_password",
                    "password1",
                    "password2",
                ),
            },
        ),
    )
    
