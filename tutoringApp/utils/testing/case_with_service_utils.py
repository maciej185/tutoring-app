"""Extenstion of TestCaseProfileUtils with creating mock Service objects."""
from datetime import datetime

from profiles.models import Profile
from tutors.models import Availability, Service, Subject

from .case_with_profile_utils import TestCaseProfileUtils


class TestCaseServiceUtils(TestCaseProfileUtils):
    """Extension of TestCaseProfileUtils class to add method for creating Service-related objects"""

    def _create_service_object(
        self,
        profile: Profile,
        subject_pk=1,
        number_of_hours=1,
        price_per_hour=100,
        session_length=60,
        is_default=True,
    ) -> Service:
        """Create single instance of the Service model.

            The function instantiates and saved custom, mock
            instance of the Service model.

        Args:
                profile: Instance of the Profile model
                        that the newly created Service
                        object will be linked to.
                subject_pk: Primary key of the Subject
                            object that the newly created
                            Service object will be linked to.
                number_of_hours: Desired value of the field of the
                                same name from the Service model.
                price_per_hour: Desired value of the field of the
                                same name from the Service model
                session_length: Desired value of the field of the
                                same name from the Service model
                is_default: Desired value of the field of the
                                same name from the Service model

        Returns:
            Newly created Service model instance.
        """
        service = Service(
            tutor=profile,
            subject=Subject.objects.get(pk=subject_pk),
            number_of_hours=number_of_hours,
            price_per_hour=price_per_hour,
            session_length=session_length,
            is_default=is_default,
        )
        service.save()
        return service

    def _create_availiability_object(
        self, service: Service, start: datetime
    ) -> Availability:
        """Create single instance of the Availability model.

        Args:
            service: Instance of the Service model that the
                    newly created Availability object will
                    relate to.
            start: Value of `start` field in the newly created
                    Availability object.

        Returns:
            Newly created Availability model instance.
        """
        availability = Availability(service=service, start=start)
        availability.save()
        return availability
