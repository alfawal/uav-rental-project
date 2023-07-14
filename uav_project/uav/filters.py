import django_filters
from uav_project.uav.models import UAVModel
from django.db import models


class UAVFilterSet(django_filters.FilterSet):
    is_rented = django_filters.BooleanFilter(method="filter_by_rented")
    price = django_filters.RangeFilter()
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
            "price",
            "created_at",
            "updated_at",
        )

    def filter_by_rented(
        self, queryset, name, value
    ) -> models.QuerySet[UAVModel]:
        return queryset.rented() if value else queryset.not_rented()
