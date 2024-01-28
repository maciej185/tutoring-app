"""Tests for the `create_appointment` view/page."""
from django.urls import reverse
from parameterized import parameterized

from lessons.models import Lesson
from profiles.models import Profile
from subscriptions.models import Appointment, ServiceSubscriptionList, Subscription
from tutors.models import Service, Subject
from utils.testing import TestCaseSubscriptionUtils


class TestCreateAppointmentView(TestCaseSubscriptionUtils):
    """Tests for the functionality of creating a new Appointment object."""

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
        self._create_servicesubscriptionlist_object(
            subscription=subscription,
            service=service,
        )

    def test_subscription_exists_user_is_related_tutor_post_request_appointment_and_lesson_objects_created(
        self,
    ):
        self.client.login(username="tutor1", password="haslo123")
        res = self.client.post(
            reverse("subscriptions:appointment_create", kwargs={"subscription_id": 1}),
            follow=True,
        )
        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(Lesson.objects.all()), 1)
        self.assertEqual(len(Appointment.objects.all()), 1)

    def test_subscription_exists_user_is_related_tutor_get_request_appointment_and_lesson_objects_not_created(
        self,
    ):
        self.client.login(username="tutor1", password="haslo123")
        res = self.client.get(
            reverse("subscriptions:appointment_create", kwargs={"subscription_id": 1}),
            follow=True,
        )
        self.assertEqual(res.status_code, 200)
        self.assertQuerySetEqual(Lesson.objects.all(), [])
        self.assertQuerySetEqual(Appointment.objects.all(), [])

    def test_subscription_exists_user_is_related_tutor_get_request_user_correctly_redirected(
        self,
    ):
        self.client.login(username="tutor1", password="haslo123")
        res = self.client.get(
            reverse("subscriptions:appointment_create", kwargs={"subscription_id": 1}),
        )
        self.assertEqual(res.status_code, 302)

    @parameterized.expand(["GET", "POST"])
    def test_subscription_does_not_exist_user_is_related_tutor_404_returned(
        self, http_method
    ):
        subscription = Subscription.objects.get(pk=1)
        subscription.delete()
        self.client.login(username="tutor1", password="haslo123")
        url = reverse("subscriptions:appointment_create", kwargs={"subscription_id": 1})
        res = self.client.get(url) if http_method == "GET" else self.client.post(url)

        self.assertEqual(res.status_code, 404)

    @parameterized.expand(
        [
            ("GET", True),
            ("GET", False),
            ("POST", True),
            ("POST", False),
        ]
    )
    def test_subscription_does_not_exist_user_is_not_related_tutor_404_returned(
        self, http_method, is_student
    ):
        subscription = Subscription.objects.get(pk=1)
        subscription.delete()
        self._register_user("user", student=is_student)
        url = reverse("subscriptions:appointment_create", kwargs={"subscription_id": 1})
        res = self.client.get(url) if http_method == "GET" else self.client.post(url)

        self.assertEqual(res.status_code, 404)

    @parameterized.expand(
        [
            ("GET", True),
            ("GET", False),
            ("POST", True),
            ("POST", False),
        ]
    )
    def test_subscription_exists_user_is_student_warning_page_displayed(
        self, http_method, is_related_student
    ):
        if not is_related_student:
            self._register_user("student")
        else:
            self.client.login(username="student1", password="haslo123")
        url = reverse("subscriptions:appointment_create", kwargs={"subscription_id": 1})
        res = self.client.get(url) if http_method == "GET" else self.client.post(url)

        self.assertEqual(res.status_code, 403)
        self.assertContains(
            res,
            "As a Student you are not allowed to create Appointments.",
            status_code=403,
        )

    @parameterized.expand(["GET", "POST"])
    def test_subscription_exists_user_is_an_unrealted_tutor_warning_page_displayed(
        self, http_method
    ):
        self._register_user("unrelated_tutor", student=False)
        url = reverse("subscriptions:appointment_create", kwargs={"subscription_id": 1})
        res = self.client.get(url) if http_method == "GET" else self.client.post(url)

        self.assertEqual(res.status_code, 403)
        self.assertContains(
            res,
            "You are not allowed to create Appointments under Subscriptions assigned to another Tutor.",
            status_code=403,
        )

    @parameterized.expand(["GET", "POST"])
    def test_subscription_exists_user_is_related_tutor_no_related_servicesubscriptionlists_warning_page_displayed(
        self, http_method
    ):
        service_subscription_list = ServiceSubscriptionList.objects.get(pk=1)
        service_subscription_list.delete()
        self.client.login(username="tutor1", password="haslo123")
        url = reverse("subscriptions:appointment_create", kwargs={"subscription_id": 1})
        res = self.client.get(url) if http_method == "GET" else self.client.post(url)

        self.assertEqual(res.status_code, 403)
        self.assertContains(
            res, "No hours left available in the Subscription.", status_code=403
        )

    @parameterized.expand(["GET", "POST"])
    def test_subscription_exists_user_is_related_tutor_related_servicesubscriptionlists_in_db_no_hours_left_warning_page_displayed(
        self, http_method
    ):
        self.client.login(username="tutor1", password="haslo123")
        url = reverse("subscriptions:appointment_create", kwargs={"subscription_id": 1})
        self.client.post(
            url
        )  # creating an appointment and thus using up all the available hours

        res = self.client.get(url) if http_method == "GET" else self.client.post(url)

        self.assertEqual(res.status_code, 403)
        self.assertContains(
            res, "No hours left available in the Subscription.", status_code=403
        )
