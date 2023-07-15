from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets

from uav_project.uav.filters import UAVFilterSet
from uav_project.uav.models import UAVModel
from uav_project.uav.serializers import UAVSerializer
from uav_project.utils.permissions import UAVPermissionMixin


class UAVViewSet(
    viewsets.ModelViewSet,
    UAVPermissionMixin,
):
    """UAV's viewset."""

    queryset = UAVModel.objects.all()
    serializer_class = UAVSerializer
    filter_backends = (
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    )
    filterset_class = UAVFilterSet
    search_fields = (
        "brand",
        "model",
        "description",
    )
    ordering_fields = (
        "created_at",
        "updated_at",
        "weight",
        "daily_price",
    )
    ordering = (
        "-created_at",
        "-updated_at",
    )
