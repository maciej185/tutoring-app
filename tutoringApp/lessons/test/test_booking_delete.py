"""Tests for the funcionality of deleting Booking objects."""

from django.urls import reverse
from freezegun import freeze_time

from lessons.models import Booking
from profiles.models import Profile
from tutors.models import Availability
from utils.testing import TestCaseBookingeUtils

NOW = "2023-12-01"
FUTURE = "2024-01-01"

from parameterized import parameterized


class TestBookingDelete(TestCaseBookingeUtils):
    """Test for the 'lessons:booking_delete' page."""

    @freeze_time(NOW)
    def test_get_request_user_is_related_student_confirmation_page_displayed(self):
        self._register_user("student1")
        student = Profile.objects.get(user__username="student1")
        self._create_booking_object(
            availability=Availability.objects.get(pk=1), student=student
        )
        self._create_booking_object(
            availability=Availability.objects.get(pk=2), student=student
        )

        res = self.client.get(reverse("lessons:booking_delete", kwargs={"pk": 1}))

        self.assertEqual(res.status_code, 200)
        self.assertContains(res, "Do you want to delete the booking?")

    @freeze_time(NOW)
    def test_post_request_user_is_related_student_booking_object_deleted_from_db(self):
        self._register_user("student1")
        student = Profile.objects.get(user__username="student1")
        self._create_booking_object(
            availability=Availability.objects.get(pk=1), student=student
        )
        self._create_booking_object(
            availability=Availability.objects.get(pk=2), student=student
        )

        self.client.post(reverse("lessons:booking_delete", kwargs={"pk": 1}))

        def get_deleted_booking_object():
            Booking.objects.get(pk=1)

        self.assertRaises(Booking.DoesNotExist, get_deleted_booking_object)

    @parameterized.expand([True, False])
    @freeze_time(NOW)
    def test_get_user_is_not_related_student_warning_page_displayed(self, is_student):
        self._register_user("student1")
        student = Profile.objects.get(user__username="student1")
        self._create_booking_object(
            availability=Availability.objects.get(pk=1), student=student
        )
        self._create_booking_object(
            availability=Availability.objects.get(pk=2), student=student
        )

        self._register_user("another_user", student=is_student)

        res = self.client.get(reverse("lessons:booking_delete", kwargs={"pk": 1}))

        self.assertEqual(res.status_code, 403)
        self.assertContains(
            res,
            "You are not allowed to delete another Student's Booking.",
            status_code=403,
            html=True,
        )

    @parameterized.expand([True, False])
    @freeze_time(NOW)
    def test_post_user_is_not_related_student_warning_page_displayed(self, is_student):
        self._register_user("student1")
        student = Profile.objects.get(user__username="student1")
        self._create_booking_object(
            availability=Availability.objects.get(pk=1), student=student
        )
        self._create_booking_object(
            availability=Availability.objects.get(pk=2), student=student
        )

        self._register_user("another_user", student=is_student)

        res = self.client.post(reverse("lessons:booking_delete", kwargs={"pk": 1}))

        self.assertEqual(res.status_code, 403)
        self.assertContains(
            res,
            "You are not allowed to delete another Student's Booking.",
            status_code=403,
            html=True,
        )

    @freeze_time(FUTURE)
    def test_get_request_user_is_related_student_related_availavility_outdated_warning_page_displayed(
        self,
    ):
        self._register_user("student1")
        student = Profile.objects.get(user__username="student1")
        self._create_booking_object(
            availability=Availability.objects.get(pk=1), student=student
        )
        self._create_booking_object(
            availability=Availability.objects.get(pk=2), student=student
        )

        res = self.client.get(reverse("lessons:booking_delete", kwargs={"pk": 1}))

        self.assertEqual(res.status_code, 403)
        self.assertContains(
            res,
            "The Availability object related to the current Booking is outdated.",
            status_code=403,
            html=True,
        )
        self.assertContains(
            res, reverse("lessons:booking_display_student"), status_code=403
        )

    @freeze_time(FUTURE)
    def test_post_request_user_is_related_student_related_availavility_outdated_warning_page_displayed(
        self,
    ):
        self._register_user("student1")
        student = Profile.objects.get(user__username="student1")
        self._create_booking_object(
            availability=Availability.objects.get(pk=1), student=student
        )
        self._create_booking_object(
            availability=Availability.objects.get(pk=2), student=student
        )

        res = self.client.post(reverse("lessons:booking_delete", kwargs={"pk": 1}))

        self.assertEqual(res.status_code, 403)
        self.assertContains(
            res,
            "The Availability object related to the current Booking is outdated.",
            status_code=403,
            html=True,
        )
        self.assertContains(
            res, reverse("lessons:booking_display_student"), status_code=403
        )
