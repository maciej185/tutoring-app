"""Extenstion of TestCaseServiceUtils allowing to create mock Subscription and Appointment objects."""
from lessons.models import Lesson
from profiles.models import Profile
from subscriptions.models import Appointment, ServiceSubscriptionList, Subscription
from tutors.models import Service, Subject

from .case_with_service_utils import TestCaseServiceUtils


class TestCaseSubscriptionUtils(TestCaseServiceUtils):
    """Extension of TestCaseServiceUtils class to add method for creating Subscription objects"""

    def setUp(self):
        """Initial database setup with Subscription-related objects."""
        self._register_user("tutor1", student=False)
        tutor1 = Profile.objects.get(user__username="tutor1")
        self._create_service_objects(profile=tutor1)
        self._register_user("student1")

    def _create_subscription_object(
        self, tutor: Profile, student: Profile, subject: Subject
    ) -> Subscription:
        """Create a mock Subscription object.

        Args:
            tutor: Instance of the Profile class representing a
                    Tutor that will be related to the newly
                    created Subscription object.
            student: Instance of the Profile class representing a
                    Student that will be related to the newly
                    created Subscription object.
            subject: Instance of the Subject class that will
                    be related to the newly created Subscription
                    object.

        Returns:
            A new instance of the Subscription model.
        """
        return Subscription.objects.create(
            tutor=tutor,
            student=student,
            subject=subject,
        )

    def _create_servicesubscriptionlist_object(
        self, subscription: Subscription, service: Service
    ) -> ServiceSubscriptionList:
        """Create a mock ServiceSubscriptionList object.

        Args:
            subscription: An instance of the Subscription model that will
                            be related to the newly created ServiceSubscriptionList
                            object.
            service: An instance of the Service model that will be related to the
                        newly created ServiceSubscriptionList object.

        Returns:
            A new instance of the ServiceSubscriptionList model.
        """
        return ServiceSubscriptionList.objects.create(
            subscription=subscription,
            service=service,
        )

    def _create_appointment_object(
        self, service_subscription_list: ServiceSubscriptionList
    ) -> Appointment:
        """Create a mock Appointment object.

        The method creates an Appointment object
        related to the provided ServiceSubscriptionList
        and an empty Lesson object that is instantiated
        right before assignment.

        Args:
            service_subscription_list: An instance of the ServiceSubscriptionList
                                        model that the newly created Appointment
                                        will be related to.
        Returns:
            A new instance of the Appointment model.
        """
        lesson = Lesson.objects.create()
        return Appointment.objects.create(
            subscription_service=service_subscription_list,
            lesson_info=lesson,
        )
