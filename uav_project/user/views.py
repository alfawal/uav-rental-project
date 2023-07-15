from django.contrib.auth import get_user_model

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, viewsets
from rest_framework.permissions import IsAuthenticated

from uav_project.user.serializers import UserSerializer


class UserViewSet(
    mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet
):
    """A viewset for listing and retrieving users."""

    queryset = get_user_model().objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer
    filter_backends = (
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    )
    search_fields = ("username", "email")
    ordering_fields = ("id", "username", "email")
    ordering = ("email",)
    filterset_fields = (
        "is_active",
        "is_superuser",
        "is_staff",
        "is_customer",
    )

    def get_queryset(self):
        """Filter the queryset based on the user.

        If the user is a superuser, return all users.
        If the user is not a superuser, return only the user itself.
        """
        qs = super().get_queryset()
        user = self.request.user

        if user.is_superuser:
            return qs

        return super().get_queryset().filter(id=self.request.user.id)
