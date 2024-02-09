"""Tests for the `subscription_create` page."""

from django.urls import reverse
from parameterized import parameterized

from profiles.models import Profile
from subscriptions.models import Subscription
from tutors.models import Availability
from utils.testing import TestCaseBookingeUtils


class TestSubscriptionCreate(TestCaseBookingeUtils):
    """Tests for the functionality of creating `Subscription` objects."""

    def setUp(self):
        """Initial database setup."""
        super().setUp()
        self._register_user("student1")

    @parameterized.expand(["GET", "POST"])
    def test_user_is_student_warning_message_displayed(self, request_type):
        self.client.login(username="student1", password="haslo123")

        url = reverse("subscriptions:subscription_create")
        res = self.client.get(url) if request_type == "GET" else self.client.post(url)

        self.assertEqual(res.status_code, 403)
        self.assertContains(
            res, "Students are not allowed to create Subscriptions.", status_code=403
        )

    def test_user_is_tutor_get_request_page_displayed(self):
        self.client.login(username="tutor1", password="haslo123")
        res = self.client.get(reverse("subscriptions:subscription_create"))

        self.assertEqual(res.status_code, 200)

    def test_user_is_tutor_get_request_correct_student_options_displayed(self):
        self._create_booking_object(
            availability=Availability.objects.get(pk=1),
            student=Profile.objects.get(user__username="student1"),
        )
        self.client.login(username="tutor1", password="haslo123")

        res = self.client.get(reverse("subscriptions:subscription_create"))

        self.assertContains(
            res,
            """<select name="student" class="options" required="" id="id_student">
                                        <option value="" selected="">---------</option>
                                        <option value="3">student1's profile</option>
                                    </select>""",
            html=True,
        )

    def test_user_is_tutor_get_request_correct_subject_options_displayed(self):
        self.client.login(username="tutor1", password="haslo123")

        res = self.client.get(reverse("subscriptions:subscription_create"))

        self.assertContains(
            res,
            """<select name="subject" class="options" required="" id="id_subject">
                                        <option value="" selected="">---------</option>
                                        <option value="1">Math</option>
                                        <option value="2">English</option>
                                    </select>""",
            html=True,
        )

    def test_user_is_tutor_provided_subject_taught_subscription_object_created(self):
        self._create_booking_object(
            availability=Availability.objects.get(pk=1),
            student=Profile.objects.get(user__username="student1"),
        )
        self.client.login(username="tutor1", password="haslo123")

        self.client.post(
            reverse("subscriptions:subscription_create"),
            data={"tutor": 1, "subject": 1, "student": 3},
            follow=True,
        )

        self.assertEqual(len(Subscription.objects.all()), 1)

    def test_user_is_tutor_subscription_already_exists_error_displayed(self):
        self._create_booking_object(
            availability=Availability.objects.get(pk=1),
            student=Profile.objects.get(user__username="student1"),
        )
        self.client.login(username="tutor1", password="haslo123")

        self.client.post(
            reverse("subscriptions:subscription_create"),
            data={"tutor": 1, "subject": 1, "student": 3},
            follow=True,
        )

        res = self.client.post(
            reverse("subscriptions:subscription_create"),
            data={"tutor": 1, "subject": 1, "student": 3},
            follow=True,
        )

        self.assertContains(
            res, "Subscription with this Tutor, Student and Subject already exists."
        )
