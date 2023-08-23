from django.contrib.auth import get_user_model

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

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

    def list(self, request, *args, **kwargs) -> Response:
        """Adds a total_count field to the response."""
        list_response = super().list(request, *args, **kwargs)
        list_response.data["total_count"] = self.get_queryset().count()
        return list_response

    @action(
        detail=False,
        methods=("get",),
        permission_classes=(IsAuthenticated,),
        url_path="me",
        url_name="users-me",
    )
    def me(self, request) -> Response:
        """Return the current logged in user details."""
        serializer = self.get_serializer(request.user)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
