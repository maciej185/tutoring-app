"""Tests for display of Tutor's profile."""
from datetime import datetime, timezone

from django.urls import reverse
from freezegun import freeze_time

from profiles.models import Profile
from tutors.models import Service
from utils.testing import TestCaseServiceUtils

NOW = "2023-12-13"


class TestDisplayTutorProfile(TestCaseServiceUtils):
    """Tests for the functionality of displaying Tutor's profile."""

    @freeze_time(NOW)
    def test_correct_current_week_displayed(self):
        self._register_user("tutor1", student=False)
        tutor = Profile.objects.get(pk=1)
        self._create_service_objects(profile=tutor)

        res = self.client.get(reverse("profiles:tutor_display", kwargs={"pk": 1}))

        days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

        for i in range(7):
            self.assertContains(
                res,
                """<div class="tutor-right-availability-main-calendar-top-element">
                                                    <div class="tutor-right-availability-main-calendar-top-element-top">
                                                        {}
                                                    </div>   
                                                    <div class="tutor-right-availability-main-calendar-top-element-bottom">
                                                        {}. Dec
                                                    </div>   
                                                </div>""".format(
                    days[i], 11 + i
                ),
                html=True,
            )

    @freeze_time(NOW)
    def test_correct_previous_week_rendered(self):
        self._register_user("tutor1", student=False)
        tutor = Profile.objects.get(pk=1)
        self._create_service_objects(profile=tutor)

        res = self.client.get(reverse("profiles:tutor_display", kwargs={"pk": 1}))

        days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

        for i in range(7):
            self.assertContains(
                res,
                """<div class="tutor-right-availability-main-calendar-top-element">
                                                    <div class="tutor-right-availability-main-calendar-top-element-top">
                                                        {}
                                                    </div>   
                                                    <div class="tutor-right-availability-main-calendar-top-element-bottom">
                                                        {}. Dec
                                                    </div>   
                                                </div>""".format(
                    days[i], f"0{4 + i}" if len(str(4 + i)) == 1 else 4 + i
                ),
                html=True,
            )

    @freeze_time(NOW)
    def test_correct_next_week_rendered(self):
        self._register_user("tutor1", student=False)
        tutor = Profile.objects.get(pk=1)
        self._create_service_objects(profile=tutor)

        res = self.client.get(reverse("profiles:tutor_display", kwargs={"pk": 1}))

        days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

        for i in range(7):
            self.assertContains(
                res,
                """<div class="tutor-right-availability-main-calendar-top-element">
                                                    <div class="tutor-right-availability-main-calendar-top-element-top">
                                                        {}
                                                    </div>   
                                                    <div class="tutor-right-availability-main-calendar-top-element-bottom">
                                                        {}. Dec
                                                    </div>   
                                                </div>""".format(
                    days[i], 18 + i
                ),
                html=True,
            )

    @freeze_time(NOW)
    def test_default_services_displayed_for_selection(self):
        self._register_user("tutor1", student=False)
        tutor = Profile.objects.get(pk=1)
        self._create_service_objects(profile=tutor)

        res = self.client.get(reverse("profiles:tutor_display", kwargs={"pk": 1}))

        self.assertContains(
            res,
            '<option value="1" selected="">Single session - Math</option>',
            html=True,
        )
        self.assertContains(
            res, '<option value="2">Single session - English</option>', html=True
        )

    @freeze_time(NOW)
    def test_non_default_services_not_displayed_for_selection(self):
        self._register_user("tutor1", student=False)
        tutor = Profile.objects.get(pk=1)
        self._create_service_objects(profile=tutor)
        self._create_service_object(
            profile=tutor, subject_pk=3, number_of_hours=10, is_default=False
        )
        self._create_service_object(
            profile=tutor, subject_pk=4, number_of_hours=10, is_default=False
        )

        res = self.client.get(reverse("profiles:tutor_display", kwargs={"pk": 1}))

        self.assertNotContains(
            res,
            '<option value="4" selected="">Single session - Physics</option>',
            html=True,
        )
        self.assertNotContains(
            res, '<option value="5">Single session - History</option>', html=True
        )

    @freeze_time(NOW)
    def test_availability_for_default_service_in_current_period_displayed(self):
        self._register_user("tutor1", student=False)
        tutor = Profile.objects.get(pk=1)
        self._create_service_objects(profile=tutor)
        service = Service.objects.get(pk=1)
        self._create_availiability_object(
            service=service, start=datetime(2023, 12, 12, 7, 0, tzinfo=timezone.utc)
        )
        self._create_availiability_object(
            service=service, start=datetime(2023, 12, 8, 8, 0, tzinfo=timezone.utc)
        )
        self._create_availiability_object(
            service=service, start=datetime(2023, 12, 22, 9, 0, tzinfo=timezone.utc)
        )

        res = self.client.get(reverse("profiles:tutor_display", kwargs={"pk": 1}))

        self.assertContains(
            res,
            """<div class="tutor-right-availability-main-calendar-bottom-column-item tutor-right-availability-main-calendar-bottom-column-item_open">
                                                    07:00
                                                </div>""",
            html=True,
        )
        self.assertContains(
            res,
            """<div class="tutor-right-availability-main-calendar-bottom-column-item tutor-right-availability-main-calendar-bottom-column-item_open">
                                                    08:00
                                                </div>""",
            html=True,
        )
        self.assertContains(
            res,
            """<div class="tutor-right-availability-main-calendar-bottom-column-item tutor-right-availability-main-calendar-bottom-column-item_open">
                                                    09:00
                                                </div>""",
            html=True,
        )

    @freeze_time(NOW)
    def test_availability_for_default_service_not_in_current_period_not_displayed(self):
        self._register_user("tutor1", student=False)
        tutor = Profile.objects.get(pk=1)
        self._create_service_objects(profile=tutor)
        service = Service.objects.get(pk=1)
        self._create_availiability_object(
            service=service, start=datetime(2023, 11, 27, 7, 0, tzinfo=timezone.utc)
        )
        self._create_availiability_object(
            service=service, start=datetime(2024, 1, 2, 8, 0, tzinfo=timezone.utc)
        )

        res = self.client.get(reverse("profiles:tutor_display", kwargs={"pk": 1}))

        self.assertNotContains(
            res,
            """<div class="tutor-right-availability-main-calendar-bottom-column-item tutor-right-availability-main-calendar-bottom-column-item_open">
                                                    07:00
                                                </div>""",
            html=True,
        )
        self.assertNotContains(
            res,
            """<div class="tutor-right-availability-main-calendar-bottom-column-item tutor-right-availability-main-calendar-bottom-column-item_open">
                                                    08:00
                                                </div>""",
            html=True,
        )

    @freeze_time(NOW)
    def test_availability_for_non_default_service_not_displayed(self):
        self._register_user("tutor1", student=False)
        tutor = Profile.objects.get(pk=1)
        self._create_service_objects(profile=tutor)
        self._create_service_object(
            profile=tutor, subject_pk=3, number_of_hours=10, is_default=False
        )
        service = Service.objects.get(pk=4)
        self._create_availiability_object(
            service=service, start=datetime(2023, 12, 12, 7, 0, tzinfo=timezone.utc)
        )
        self._create_availiability_object(
            service=service, start=datetime(2023, 12, 8, 8, 0, tzinfo=timezone.utc)
        )
        self._create_availiability_object(
            service=service, start=datetime(2023, 12, 22, 9, 0, tzinfo=timezone.utc)
        )

        res = self.client.get(reverse("profiles:tutor_display", kwargs={"pk": 1}))

        self.assertNotContains(
            res,
            """<div class="tutor-right-availability-main-calendar-bottom-column-item tutor-right-availability-main-calendar-bottom-column-item_open">
                                                    07:00
                                                </div>""",
            html=True,
        )
        self.assertNotContains(
            res,
            """<div class="tutor-right-availability-main-calendar-bottom-column-item tutor-right-availability-main-calendar-bottom-column-item_open">
                                                    08:00
                                                </div>""",
            html=True,
        )
        self.assertNotContains(
            res,
            """<div class="tutor-right-availability-main-calendar-bottom-column-item tutor-right-availability-main-calendar-bottom-column-item_open">
                                                    09:00
                                                </div>""",
            html=True,
        )
