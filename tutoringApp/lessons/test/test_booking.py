"""Tests for the functionality of booking single sessions."""
from datetime import datetime, timezone

from django.urls import reverse
from freezegun import freeze_time

from lessons.models import Booking, Lesson
from profiles.models import Profile
from tutors.models import Service
from utils.testing import TestCaseServiceUtils

NOW = "2023-12-13 07:59:00"


class TestBooking(TestCaseServiceUtils):
    """Tests for the functionality of booking single sessions."""

    @freeze_time(NOW)
    def test_availability_object_exists_booking_page_displayed(self):
        self._register_user("tutor1", student=False)
        tutor = Profile.objects.get(user__username="tutor1")
        self._create_service_objects(profile=tutor)
        service1 = Service.objects.get(pk=1)
        self._create_availiability_object(
            service=service1, start=datetime(2023, 12, 14, 8, 0, tzinfo=timezone.utc)
        )
        self._register_user("student1")
        self.client.logout()
        self.client.login(username="student1", password="haslo123")

        res = self.client.get(
            reverse("lessons:booking_create", kwargs={"availability_id": 1})
        )

        self.assertEqual(res.status_code, 200)

    def test_availability_object_exists_post_request_sent_booking_object_created(self):
        self._register_user("tutor1", student=False)
        tutor = Profile.objects.get(user__username="tutor1")
        self._create_service_objects(profile=tutor)
        service1 = Service.objects.get(pk=1)
        self._create_availiability_object(
            service=service1, start=datetime(2023, 12, 12, 8, 0, tzinfo=timezone.utc)
        )
        self._register_user("student1")
        self.client.logout()
        self.client.login(username="student1", password="haslo123")

        self.assertQuerySetEqual(Booking.objects.all(), [])

        res = self.client.post(
            reverse("lessons:booking_create", kwargs={"availability_id": 1})
        )

        self.assertEqual(res.status_code, 302)
        self.assertEqual(len(Booking.objects.all()), 1)

    def test_availability_object_exists_post_request_sent_lesson_object_created(self):
        self._register_user("tutor1", student=False)
        tutor = Profile.objects.get(user__username="tutor1")
        self._create_service_objects(profile=tutor)
        service1 = Service.objects.get(pk=1)
        self._create_availiability_object(
            service=service1, start=datetime(2023, 12, 12, 8, 0, tzinfo=timezone.utc)
        )
        self._register_user("student1")
        self.client.logout()
        self.client.login(username="student1", password="haslo123")

        self.assertQuerySetEqual(Lesson.objects.all(), [])

        res = self.client.post(
            reverse("lessons:booking_create", kwargs={"availability_id": 1})
        )

        self.assertEqual(res.status_code, 302)
        self.assertEqual(len(Lesson.objects.all()), 1)

    def test_user_is_tutor_warning_page_displayed(self):
        self._register_user("tutor1", student=False)
        tutor = Profile.objects.get(user__username="tutor1")
        self._create_service_objects(profile=tutor)
        service1 = Service.objects.get(pk=1)
        self._create_availiability_object(
            service=service1, start=datetime(2023, 12, 12, 8, 0, tzinfo=timezone.utc)
        )
        self._register_user("tutor2", student=False)
        self.client.logout()
        self.client.login(username="tutor2", password="haslo123")

        res = self.client.get(
            reverse("lessons:booking_create", kwargs={"availability_id": 1})
        )

        self.assertEqual(res.status_code, 403)
        self.assertContains(
            res,
            "Tutors are not allowed to book sessions with other tutors.",
            status_code=403,
        )

    def test_availability_object_does_not_exist_warning_page_displayed(self):
        self._register_user("student1")

        res = self.client.get(
            reverse("lessons:booking_create", kwargs={"availability_id": 1})
        )

        self.assertEqual(res.status_code, 404)
        self.assertContains(
            res,
            "Availability object with provided primary key does not exist.",
            status_code=404,
        )

    def test_booking_relating_to_given_availability_exists_warning_page_displayed(self):
        self._register_user("tutor1", student=False)
        tutor = Profile.objects.get(user__username="tutor1")
        self._create_service_objects(profile=tutor)
        service1 = Service.objects.get(pk=1)
        self._create_availiability_object(
            service=service1, start=datetime(2023, 12, 12, 8, 0, tzinfo=timezone.utc)
        )
        self._register_user("student1")
        self.client.logout()
        self.client.login(username="student1", password="haslo123")

        self.assertQuerySetEqual(Booking.objects.all(), [])

        res_post = self.client.post(
            reverse("lessons:booking_create", kwargs={"availability_id": 1})
        )

        self.assertEqual(res_post.status_code, 302)

        res_get = self.client.get(
            reverse("lessons:booking_create", kwargs={"availability_id": 1})
        )

        self.assertEqual(res_get.status_code, 404)
        self.assertContains(
            res_get,
            "Booking related to Availability with provided ID already exists.",
            status_code=404,
        )

    @freeze_time(NOW)
    def test_availability_object_outdated_warning_displayed(self):
        self._register_user("tutor1", student=False)
        tutor = Profile.objects.get(user__username="tutor1")
        self._create_service_objects(profile=tutor)
        service1 = Service.objects.get(pk=1)
        self._create_availiability_object(
            service=service1, start=datetime(2023, 12, 12, 8, 0, tzinfo=timezone.utc)
        )
        self._register_user("student1")
        self.client.logout()
        self.client.login(username="student1", password="haslo123")

        res = self.client.get(
            reverse("lessons:booking_create", kwargs={"availability_id": 1})
        )

        self.assertEqual(res.status_code, 403)
        self.assertContains(
            res,
            "Availability is outdated. Please choose another available time slot.",
            status_code=403,
        )
