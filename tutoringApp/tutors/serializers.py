"""Serializers for models from the `Tutors` app."""
from datetime import datetime, timedelta, timezone
from typing import Any

from rest_framework import serializers

from tutors.models import Availability
from tutors.time_range import TimeRange


def time_slot_conflict(
    first_start: datetime,
    first_end: datetime,
    second_start: datetime,
    second_end: datetime,
) -> bool:
    """Check if the first time slot conflicts with the second one."""


def get_end_time(start_time, sessions_duration) -> datetime:
    """Calculate the end time."""


class AvailabilitySerializer(serializers.ModelSerializer):
    """Serializer for the Availability model."""

    class Meta:
        model = Availability
        fields = "__all__"

    def validate(self, data: dict[Any, Any]) -> dict[Any, Any]:
        """Check if given Tutor does not have conflicting sessions available.

        The method fetches all Availability objects for a tutor
        related to Service whose PK has been sent in the request
        and checks if the provided time does not conflict with any
        of the already existing Availability objects. An additional
        check to ensure the entire session lies in the future is also
        made.

        Args:
            data: Dictionary of field values.

        Raises:
            serializers.ValidationError when an Availability object with a conflicting
            time is already present in the database or when the end of the tutoring
            session falls in the past.

        Returns:
            Initial dictionary of field values if no error was raised.
        """
        availabilites = Availability.objects.filter(
            service__tutor=data["service"].tutor
        )
        start_time_range = TimeRange.from_start_and_duration(
            data["start"], timedelta(minutes=data["service"].session_length)
        )
        if any(
            [
                (start_time_range in availability.time_range)
                for availability in availabilites
            ]
        ):
            raise serializers.ValidationError(
                "There is an Availability object with a conflicting time slot already in the database."
            )
        if (
            data["start"] + timedelta(minutes=data["service"].session_length)
        ) < datetime.now(tz=timezone.utc):
            raise serializers.ValidationError(
                "Given time slot falls in the past. Please input valid start time."
            )

        return data
