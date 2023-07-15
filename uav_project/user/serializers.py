from django.contrib.auth import get_user_model

from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    """User serializer."""

    class Meta:
        """Meta class."""

        model = get_user_model()
        fields = (
            "id",
            "username",
            "email",
            "is_active",
            "is_superuser",
            "is_staff",
            "is_customer",
        )
