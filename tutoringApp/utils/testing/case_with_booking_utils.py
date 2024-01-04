"""Extenstion of TestCaseServiceUtils allowing to create mock Booking objects."""

from datetime import datetime, timezone

from freezegun import freeze_time

from lessons.models import Booking, Lesson
from profiles.models import Profile
from tutors.models import Availability, Service

from .case_with_service_utils import TestCaseServiceUtils

NOW = "2023-12-13 07:59:00+00:00"


class TestCaseBookingeUtils(TestCaseServiceUtils):
    """Extension of TestCaseServiceUtils class to add method for creating Booking-related objects"""

    @freeze_time(NOW)
    def setUp(cls):
        """Initial database setup."""
        cls._register_user("tutor1", student=False)
        tutor1 = Profile.objects.get(user__username="tutor1")
        cls._create_service_objects(profile=tutor1)
        service1 = Service.objects.get(pk=1)
        cls._create_availiability_object(
            service=service1, start=datetime(2023, 12, 12, 8, 0, tzinfo=timezone.utc)
        )
        cls._create_availiability_object(
            service=service1, start=datetime(2023, 12, 14, 9, 0, tzinfo=timezone.utc)
        )
        cls._create_availiability_object(
            service=service1, start=datetime(2023, 12, 14, 10, 0, tzinfo=timezone.utc)
        )
        cls._create_availiability_object(
            service=service1, start=datetime(2023, 12, 14, 11, 0, tzinfo=timezone.utc)
        )
        cls._create_availiability_object(
            service=service1, start=datetime(2023, 12, 15, 8, 0, tzinfo=timezone.utc)
        )
        cls._create_availiability_object(
            service=service1, start=datetime(2023, 12, 16, 8, 0, tzinfo=timezone.utc)
        )

        cls._register_user("tutor2", student=False)
        tutor2 = Profile.objects.get(user__username="tutor2")
        cls._create_service_objects(profile=tutor2)
        service2 = Service.objects.get(pk=4)
        cls._create_availiability_object(
            service=service2, start=datetime(2023, 12, 10, 8, 0, tzinfo=timezone.utc)
        )
        cls._create_availiability_object(
            service=service2, start=datetime(2023, 12, 12, 8, 0, tzinfo=timezone.utc)
        )
        cls._create_availiability_object(
            service=service2, start=datetime(2023, 12, 14, 9, 0, tzinfo=timezone.utc)
        )
        cls._create_availiability_object(
            service=service2, start=datetime(2023, 12, 14, 10, 0, tzinfo=timezone.utc)
        )
        cls._create_availiability_object(
            service=service2, start=datetime(2023, 12, 14, 11, 0, tzinfo=timezone.utc)
        )
        cls._create_availiability_object(
            service=service2, start=datetime(2023, 12, 17, 8, 0, tzinfo=timezone.utc)
        )

    def _create_booking_object(
        self, availability: Availability, student: Profile
    ) -> Booking:
        """Create and save Booking object related to provided Availability.

        Args:
            availability: Instance of the Availability model
                            that the newly created Booking object
                            will be related to.
            student: Instance of the Profile model
                            that the newly created Booking object
                            will be related to.
        Returns:
            Newly created instance of the Booking model.
        """
        lesson = Lesson(date=availability.start)
        lesson.save()

        booking = Booking(
            lesson_info=lesson,
            availability=availability,
            student=student,
        )
        booking.save()

        return booking
