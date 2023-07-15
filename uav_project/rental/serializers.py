from rest_framework import serializers

from uav_project.rental.models import Rental


class RentalSerializer(serializers.ModelSerializer):
    total_price = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Rental
        read_only_fields = (
            "id",
            "uav",
            "price",
            "total_price",
            "created_at",
            "updated_at",
        )
        fields = (
            "start_date",
            "end_date",
        ) + read_only_fields

    def validate(self, data: dict) -> dict:
        """Set the user and uav on creation based on the url."""
        current_object = self.instance
        is_creation = current_object is None
        if is_creation:
            data["user"] = self.context["request"].user
            data["uav"] = self.context["view"].kwargs["uav_pk"]

        return data

    def get_total_price(self, obj: Rental) -> str:
        """Calculate the total price of the rental."""
        return obj.get_total_price()
