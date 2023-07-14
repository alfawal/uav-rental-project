from rest_framework import viewsets, mixins, filters
from django_filters.rest_framework import DjangoFilterBackend
from uav_project.uav.filters import UAVFilterSet
from uav_project.uav.models import UAVModel


class UAVListViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """UAVs listing viewset."""

    queryset = UAVModel.objects.all()
    serializer_class = ...  # TODO: Add serializer class
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
        "price",
    )
    ordering = ("-created_at", "-updated_at")
