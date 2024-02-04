"""Tests for the `appointment_delete` page."""

from django.urls import reverse
from parameterized import parameterized

from profiles.models import Profile
from subscriptions.models import Appointment
from tutors.models import Service, Subject
from utils.testing import TestCaseSubscriptionUtils


class TestDeleteAppointmentView(TestCaseSubscriptionUtils):
    """Tests for the functionality of deleting Appointment objects."""

    def setUp(self):
        """Initial database setup."""
        super().setUp()
        tutor = Profile.objects.get(user__username="tutor1")
        student = Profile.objects.get(user__username="student1")
        subject = Subject.objects.get(pk=1)
        subscription = self._create_subscription_object(
            tutor=tutor, student=student, subject=subject
        )

        service = Service.objects.get(pk=1)
        self.service_subscription_list = self._create_servicesubscriptionlist_object(
            subscription=subscription,
            service=service,
        )

    @parameterized.expand(
        [("tutor1", "haslo123"), ("student1", "haslo123"), ("tutor2", "haslo123")]
    )
    def test_appointment_does_not_exist_404_returned(self, username, password):
        self.client.login(username=username, password=password)
        res = self.client.get(
            reverse("subscriptions:appointment_delete", kwargs={"pk": 1})
        )
        self.assertEqual(res.status_code, 404)

    @parameterized.expand(
        [
            ("GET", "student1", "haslo123"),
            ("GET", "tutor2", "haslo123"),
            ("POST", "student1", "haslo123"),
            ("POST", "tutor2", "haslo123"),
        ]
    )
    def test_user_is_not_related_tutor_warning_page_displayed(
        self, request_type, username, password
    ):
        self._create_appointment_object(
            service_subscription_list=self.service_subscription_list
        )
        self.client.login(username=username, password=password)
        res_url = reverse("subscriptions:appointment_delete", kwargs={"pk": 1})
        res = (
            self.client.get(res_url)
            if request_type == "GET"
            else self.client.post(res_url)
        )
        self.assertEqual(res.status_code, 403)
        self.assertContains(
            res, "You are not allowed to delete the Appointment.", status_code=403
        )

    def test_user_is_related_tutor_get_request_confirmation_page_displayed(self):
        self._create_appointment_object(
            service_subscription_list=self.service_subscription_list
        )
        self.client.login(username="tutor1", password="haslo123")
        res = self.client.get(
            reverse("subscriptions:appointment_delete", kwargs={"pk": 1})
        )
        self.assertEqual(res.status_code, 200)
        self.assertContains(res, "Do you want to cancel the Appointment?")

    def test_user_is_related_tutor_post_request_appointment_object_deleted_from_db(
        self,
    ):
        self._create_appointment_object(
            service_subscription_list=self.service_subscription_list
        )
        self.client.login(username="tutor1", password="haslo123")
        res = self.client.post(
            reverse("subscriptions:appointment_delete", kwargs={"pk": 1})
        )
        self.assertEqual(res.status_code, 302)
        self.assertQuerySetEqual(Appointment.objects.all(), [])

    def test_user_is_related_tutor_post_request_user_correctly_redirected(self):
        self._create_appointment_object(
            service_subscription_list=self.service_subscription_list
        )
        self.client.login(username="tutor1", password="haslo123")
        res = self.client.post(
            reverse("subscriptions:appointment_delete", kwargs={"pk": 1}), follow=True
        )

        self.assertRedirects(
            res, reverse("subscriptions:learning_tutor", kwargs={"subscription_id": 1})
        )
