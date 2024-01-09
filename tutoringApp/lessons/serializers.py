"""Serializers for endpoints in the `lessons` app."""

from rest_framework import serializers

from lessons.models import Solution


class SolutionSerializer(serializers.ModelSerializer):
    """Serializer for the Solution model."""

    class Meta:
        model = Solution
        fields = ["task", "solution"]
