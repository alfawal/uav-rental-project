from django.contrib import admin

from uav_project.rental.models import Rental


@admin.register(Rental)
class RentalAdmin(admin.ModelAdmin):
    verbose_name = "Rental"
    verbose_name_plural = "Rentals"
    list_display = ("id", "uav", "user", "start_date", "end_date", "price")
    list_display_links = ("id", "uav", "user")
    list_filter = ("user",)
    search_fields = ("id", "uav", "price")
    ordering = ("-created_at", "-updated_at")
    readonly_fields = ("id", "price")
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "id",
                    "uav",
                    "start_date",
                    "end_date",
                    "price",
                )
            },
        ),
    )
