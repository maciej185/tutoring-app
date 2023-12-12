"""Serializers for models from the `Tutors` app."""
from rest_framework import serializers

from tutors.models import Availability


class AvailabilitySerializer(serializers.ModelSerializer):
    """Serializer for the Availability model."""

    class Meta:
        model = Availability
        fields = "__all__"
