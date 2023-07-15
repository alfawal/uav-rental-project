from django.db import models

import django_filters

from uav_project.uav.models import UAVModel


class UAVFilterSet(django_filters.FilterSet):
    is_rented = django_filters.BooleanFilter(
        field_name="is_rented", label="Is rented?", method="filter_by_rented"
    )
    daily_price = django_filters.RangeFilter()
    weight = django_filters.RangeFilter()
    created_at = django_filters.DateTimeFromToRangeFilter()
    updated_at = django_filters.DateTimeFromToRangeFilter()

    class Meta:
        model = UAVModel
        fields = (
            "is_rented",
            "brand",
            "model",
            "weight",
            "category",
            "description",
            "daily_price",
            "created_at",
            "updated_at",
        )

    def filter_by_rented(
        self, queryset, name, value
    ) -> models.QuerySet[UAVModel]:
        return queryset.rented() if value else queryset.not_rented()
