from rest_framework import filters, viewsets

from uav_project.rental.models import Rental
from uav_project.rental.serializers import RentalSerializer


class RentalViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows rentals to be viewed or edited.
    """

    queryset = Rental.objects.all().select_related("uav", "user")
    serializer_class = RentalSerializer
    filter_backends = (filters.OrderingFilter,)
    ordering_fields = (
        "created_at",
        "updated_at",
        "start_date",
        "end_date",
    )
    ordering = (
        "-created_at",
        "-updated_at",
    )

    def get_queryset(self):
        """Filter the queryset based on the user and uav_pk.

        If the user is a customer, filter the queryset based on the user.
        Otherwise (when admin), list all of the rentals by all of the users.
        """
        qs = super().get_queryset()
        user = self.request.user

        if user.is_customer:
            qs = qs.filter(user=user)
        elif user_pk := self.kwargs.get("user_pk"):
            qs = qs.filter(user_id=user_pk)

        if uav_pk := self.kwargs.get("uav_pk"):
            qs = qs.filter(uav_id=uav_pk)

        return qs
