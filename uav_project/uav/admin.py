from django.contrib import admin
from django.utils.html import escape
from django.utils.safestring import mark_safe

from uav_project.uav.models import UAVModel
from uav_project.utils.admin import JSONWidgetAdmin


@admin.register(UAVModel)
class UAVAdmin(JSONWidgetAdmin):
    verbose_name = "UAV"
    verbose_name_plural = "UAVs"
    list_display = (
        "brand",
        "model",
        "weight",
        "category",
        "daily_price",
    )
    list_display_links = ("brand", "model")
    list_filter = ("model",)
    search_fields = ("brand", "model")
    ordering = ("brand",)
    readonly_fields = ("id", "image_tag")
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "id",
                    "brand",
                    "model",
                    "weight",
                    "category",
                    "description",
                    "daily_price",
                    "photo",
                    "image_tag",
                    "data",
                )
            },
        ),
    )

    def image_tag(self, obj):
        return mark_safe(f'<img src="{escape(obj.photo.url)}" width="512" />')

    image_tag.short_description = "Photo Preview"
