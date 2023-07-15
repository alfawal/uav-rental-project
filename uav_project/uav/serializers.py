from rest_framework import serializers

from uav_project.uav.models import UAVModel


class UAVSerializer(serializers.ModelSerializer):
    """UAVs listing serializer."""

    class Meta:
        """Meta class."""

        model = UAVModel
        fields = (
            "id",
            "brand",
            "model",
            "weight",
            "category",
            "description",
            "daily_price",
            "photo",
            "data",
        )
