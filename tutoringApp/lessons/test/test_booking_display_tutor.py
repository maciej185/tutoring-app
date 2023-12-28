"""Tests for the funcionality of displaying booked sessions by a Tutor."""
from django.urls import reverse
from freezegun import freeze_time

from profiles.models import Profile
from tutors.models import Availability
from utils.testing import TestCaseBookingeUtils

NOW = "2023-12-13 07:59:00"


class TestBookingDisplayTutor(TestCaseBookingeUtils):
    """Tests for the funcionality of displaying booked sessions by a Tutor."""

    @freeze_time(NOW)
    def test_session_booked_displayed_on_page(self):
        self._register_user("student1")
        student = Profile.objects.get(user__username="student1")
        availability = Availability.objects.get(pk=1)
        self._create_booking_object(availability=availability, student=student)

        self.client.login(username="tutor1", password="haslo123")
        res = self.client.get(reverse("lessons:booking_display_tutor"))

        self.assertEqual(res.status_code, 200)
        self.assertContains(res, "Single Math session with student1")

    @freeze_time(NOW)
    def test_session_in_future_cancel_button_not_displayed(self):
        self._register_user("student1")
        student = Profile.objects.get(user__username="student1")
        availability = Availability.objects.get(pk=3)
        self._create_booking_object(availability=availability, student=student)

        self.client.login(username="tutor1", password="haslo123")
        res = self.client.get(reverse("lessons:booking_display_tutor"))

        self.assertEqual(res.status_code, 200)
        self.assertNotContains(res, reverse("lessons:booking_delete", kwargs={"pk": 1}))

    @freeze_time(NOW)
    def test_session_in_past_cancel_button_not_displayed(self):
        self._register_user("student1")
        student = Profile.objects.get(user__username="student1")
        availability = Availability.objects.get(pk=1)
        self._create_booking_object(availability=availability, student=student)

        self.client.login(username="tutor1", password="haslo123")
        res = self.client.get(reverse("lessons:booking_display_tutor"))

        self.assertEqual(res.status_code, 200)
        self.assertNotContains(res, reverse("lessons:booking_delete", kwargs={"pk": 1}))

    def test_booking_objects_created_correct_student_filter_options_displayed(self):
        self._register_user("student1")
        self._register_user("student2")
        student1 = Profile.objects.get(user__username="student1")
        student2 = Profile.objects.get(user__username="student2")
        self._create_booking_object(
            availability=Availability.objects.get(pk=1), student=student1
        )
        self._create_booking_object(
            availability=Availability.objects.get(pk=2), student=student1
        )
        self._create_booking_object(
            availability=Availability.objects.get(pk=3), student=student2
        )
        self._create_booking_object(
            availability=Availability.objects.get(pk=4), student=student2
        )

        self.client.login(username="tutor1", password="haslo123")
        res = self.client.get(reverse("lessons:booking_display_tutor"))

        self.assertContains(res, '<option value="3">student1</option>', html=True)
        self.assertContains(res, '<option value="4">student2</option>', html=True)

    @freeze_time(NOW)
    def test_from_url_query_parameter_passed_booking_objects_filtered(self):
        self._register_user("student1")
        student = Profile.objects.get(user__username="student1")
        self._create_booking_object(
            availability=Availability.objects.get(pk=1), student=student
        )
        self._create_booking_object(
            availability=Availability.objects.get(pk=4), student=student
        )
        self._create_booking_object(
            availability=Availability.objects.get(pk=5), student=student
        )
        self._create_booking_object(
            availability=Availability.objects.get(pk=6), student=student
        )

        self.client.login(username="tutor1", password="haslo123")
        res = self.client.get(
            reverse("lessons:booking_display_tutor") + "?from=2023-12-14"
        )

        self.assertEqual(res.status_code, 200)
        self.assertNotContains(res, "12. Dec 2023, 08:00-09:00")
        self.assertContains(res, "14. Dec 2023, 11:00-12:00")
        self.assertContains(res, "15. Dec 2023, 08:00-09:00")
        self.assertContains(res, "16. Dec 2023, 08:00-09:00")

    @freeze_time(NOW)
    def test_to_url_query_parameter_passed_booking_objects_filtered(self):
        self._register_user("student1")
        student = Profile.objects.get(user__username="student1")
        self._create_booking_object(
            availability=Availability.objects.get(pk=1), student=student
        )
        self._create_booking_object(
            availability=Availability.objects.get(pk=4), student=student
        )
        self._create_booking_object(
            availability=Availability.objects.get(pk=5), student=student
        )
        self._create_booking_object(
            availability=Availability.objects.get(pk=6), student=student
        )

        self.client.login(username="tutor1", password="haslo123")
        res = self.client.get(
            reverse("lessons:booking_display_tutor") + "?to=2023-12-14"
        )

        self.assertEqual(res.status_code, 200)
        self.assertContains(res, "12. Dec 2023, 08:00-09:00")
        self.assertContains(res, "14. Dec 2023, 11:00-12:00")
        self.assertNotContains(res, "15. Dec 2023, 08:00-09:00")
        self.assertNotContains(res, "16. Dec 2023, 08:00-09:00")

    def test_profile_url_query_parameter_passed_booking_objects_filtered(self):
        self._register_user("student1")
        self._register_user("student2")
        student1 = Profile.objects.get(user__username="student1")
        student2 = Profile.objects.get(user__username="student2")
        self._create_booking_object(
            availability=Availability.objects.get(pk=1), student=student1
        )
        self._create_booking_object(
            availability=Availability.objects.get(pk=2), student=student1
        )
        self._create_booking_object(
            availability=Availability.objects.get(pk=3), student=student2
        )
        self._create_booking_object(
            availability=Availability.objects.get(pk=4), student=student2
        )

        self.client.login(username="tutor1", password="haslo123")
        res = self.client.get(reverse("lessons:booking_display_tutor") + "?profile=4")

        self.assertNotContains(res, "12. Dec 2023, 08:00-09:00")
        self.assertNotContains(res, "14. Dec 2023, 09:00-10:00")
        self.assertContains(res, "14. Dec 2023, 10:00-11:00")
        self.assertContains(res, "14. Dec 2023, 11:00-12:00")

    def test_from_and_to_url_query_parameters_passed_booking_objects_filtered_correctly(
        self,
    ):
        self._register_user("student1")
        student = Profile.objects.get(user__username="student1")
        self._create_booking_object(
            availability=Availability.objects.get(pk=7), student=student
        )
        self._create_booking_object(
            availability=Availability.objects.get(pk=8), student=student
        )
        self._create_booking_object(
            availability=Availability.objects.get(pk=9), student=student
        )
        self._create_booking_object(
            availability=Availability.objects.get(pk=10), student=student
        )
        self._create_booking_object(
            availability=Availability.objects.get(pk=11), student=student
        )
        self._create_booking_object(
            availability=Availability.objects.get(pk=12), student=student
        )

        self.client.login(username="tutor2", password="haslo123")
        res = self.client.get(
            reverse("lessons:booking_display_tutor") + "?from=2023-12-12&to=2023-12-14"
        )

        self.assertNotContains(res, "10. Dec 2023, 08:00-09:00")
        self.assertContains(res, "12. Dec 2023, 08:00-09:00")
        self.assertContains(res, "14. Dec 2023, 09:00-10:00")
        self.assertContains(res, "14. Dec 2023, 10:00-11:00")
        self.assertContains(res, "14. Dec 2023, 11:00-12:00")
        self.assertNotContains(res, "17. Dec 2023, 08:00-09:00")

    def test_from_and_profile_url_query_parameters_passed_booking_objects_filtered_correctly(
        self,
    ):
        self._register_user("student1")
        self._register_user("student2")
        student1 = Profile.objects.get(user__username="student1")
        student2 = Profile.objects.get(user__username="student2")
        self._create_booking_object(
            availability=Availability.objects.get(pk=1), student=student1
        )
        self._create_booking_object(
            availability=Availability.objects.get(pk=2), student=student1
        )
        self._create_booking_object(
            availability=Availability.objects.get(pk=3), student=student1
        )
        self._create_booking_object(
            availability=Availability.objects.get(pk=4), student=student2
        )
        self._create_booking_object(
            availability=Availability.objects.get(pk=5), student=student2
        )
        self._create_booking_object(
            availability=Availability.objects.get(pk=6), student=student2
        )

        self.client.login(username="tutor1", password="haslo123")
        res = self.client.get(
            reverse("lessons:booking_display_tutor") + "?from=2023-12-14&profile=4"
        )

        self.assertNotContains(res, "12. Dec 2023, 08:00-09:00")
        self.assertNotContains(res, "14. Dec 2023, 09:00-10:00")
        self.assertNotContains(res, "14. Dec 2023, 10:00-11:00")
        self.assertContains(res, "14. Dec 2023, 11:00-12:00")
        self.assertContains(res, "15. Dec 2023, 08:00-09:00")
        self.assertContains(res, "16. Dec 2023, 08:00-09:00")

    def test_to_and_profile_url_query_parameters_passed_booking_objects_filtered_correctly(
        self,
    ):
        self._register_user("student1")
        self._register_user("student2")
        student1 = Profile.objects.get(user__username="student1")
        student2 = Profile.objects.get(user__username="student2")
        self._create_booking_object(
            availability=Availability.objects.get(pk=1), student=student1
        )
        self._create_booking_object(
            availability=Availability.objects.get(pk=2), student=student1
        )
        self._create_booking_object(
            availability=Availability.objects.get(pk=3), student=student1
        )
        self._create_booking_object(
            availability=Availability.objects.get(pk=4), student=student2
        )
        self._create_booking_object(
            availability=Availability.objects.get(pk=5), student=student2
        )
        self._create_booking_object(
            availability=Availability.objects.get(pk=6), student=student2
        )

        self.client.login(username="tutor1", password="haslo123")
        res = self.client.get(
            reverse("lessons:booking_display_tutor") + "?to=2023-12-15&profile=3"
        )

        self.assertContains(res, "12. Dec 2023, 08:00-09:00")
        self.assertContains(res, "14. Dec 2023, 09:00-10:00")
        self.assertContains(res, "14. Dec 2023, 10:00-11:00")
        self.assertNotContains(res, "14. Dec 2023, 11:00-12:00")
        self.assertNotContains(res, "15. Dec 2023, 08:00-09:00")
        self.assertNotContains(res, "16. Dec 2023, 08:00-09:00")

    def test_from_and_to_and_profile_url_query_parameters_passed_booking_objects_filtered_correctly(
        self,
    ):
        self._register_user("student1")
        self._register_user("student2")
        student1 = Profile.objects.get(user__username="student1")
        student2 = Profile.objects.get(user__username="student2")
        self._create_booking_object(
            availability=Availability.objects.get(pk=7), student=student2
        )
        self._create_booking_object(
            availability=Availability.objects.get(pk=8), student=student1
        )
        self._create_booking_object(
            availability=Availability.objects.get(pk=9), student=student1
        )
        self._create_booking_object(
            availability=Availability.objects.get(pk=10), student=student2
        )
        self._create_booking_object(
            availability=Availability.objects.get(pk=11), student=student2
        )
        self._create_booking_object(
            availability=Availability.objects.get(pk=12), student=student2
        )

        self.client.login(username="tutor2", password="haslo123")
        res = self.client.get(
            reverse("lessons:booking_display_tutor")
            + "?from=2023-12-12&to=2023-12-14&profile=4"
        )

        self.assertNotContains(res, "10. Dec 2023, 08:00-09:00")
        self.assertNotContains(res, "12. Dec 2023, 08:00-09:00")
        self.assertNotContains(res, "14. Dec 2023, 09:00-10:00")
        self.assertContains(res, "14. Dec 2023, 10:00-11:00")
        self.assertContains(res, "14. Dec 2023, 11:00-12:00")
        self.assertNotContains(res, "17. Dec 2023, 08:00-09:00")

    def test_requesting_display_bookings_for_student_user_redirected_to_display_bookings_for_tutor(
        self,
    ):
        self.client.login(username="tutor2", password="haslo123")

        res = self.client.get(reverse("lessons:booking_display_student"))

        self.assertEqual(res.status_code, 302)
        self.assertRedirects(res, reverse("lessons:booking_display_tutor"))
