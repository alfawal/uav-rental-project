from django.contrib import admin
from django.contrib.auth.models import Group

from uav_project.user.models import UAVUser

admin.site.unregister(Group)


@admin.register(UAVUser)
class UAVUserAdmin(admin.ModelAdmin):
    verbose_name = "User"
    verbose_name_plural = "Users"
    list_display = (
        "username",
        "email",
        "is_active",
        "last_login",
        "is_superuser",
        "is_staff",
        "is_customer",
    )
    list_display_links = ("username", "email")
    list_filter = (
        "is_active",
        "is_superuser",
        "is_staff",
        "is_customer",
    )
    search_fields = ("username", "email")
    ordering = ("username",)
    readonly_fields = (
        "id",
        "password",
    )
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "id",
                    "username",
                    "email",
                    "password",
                    "is_active",
                )
            },
        ),
        (
            "Permissions",
            {
                "fields": (
                    "is_superuser",
                    "is_staff",
                    "is_customer",
                )
            },
        ),
    )
