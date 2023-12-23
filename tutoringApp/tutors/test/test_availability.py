"""Test for availability input views."""
from datetime import datetime, timezone

from django.urls import reverse
from freezegun import freeze_time

from profiles.models import Profile
from tutors.models import Availability, Service
from utils.testing import TestCaseServiceUtils

NOW = "2023-12-13 07:59:00"


class TestAvailabilityInputView(TestCaseServiceUtils):
    """Tests for the availability input page."""

    def test_default_services_displayed_on_page(self):
        self._register_user("tutor1", student=False)
        tutor = Profile.objects.get(pk=1)
        self._create_service_objects(profile=tutor)
        self._create_service_object(
            profile=tutor, subject_pk=3, number_of_hours=10, is_default=False
        )

        res = self.client.get(
            reverse("tutors:availability", kwargs={"pk": 1, "month": 12, "year": 2023})
        )

        self.assertContains(res, "Math")
        self.assertContains(res, "English")

    def test_non_defuault_services_not_displayed_on_page(self):
        self._register_user("tutor1", student=False)
        tutor = Profile.objects.get(pk=1)
        self._create_service_objects(profile=tutor)
        self._create_service_object(
            profile=tutor, subject_pk=3, number_of_hours=10, is_default=False
        )
        self._create_service_object(
            profile=tutor, subject_pk=4, number_of_hours=10, is_default=False
        )

        res = self.client.get(
            reverse("tutors:availability", kwargs={"pk": 1, "month": 12, "year": 2023})
        )

        self.assertNotContains(res, "Physics")
        self.assertNotContains(res, "History")

    def test_correct_session_length_displayed_on_page(self):
        self._register_user("tutor1", student=False)
        tutor = Profile.objects.get(pk=1)
        self._create_service_objects(profile=tutor)
        self._create_service_object(profile=tutor, subject_pk=4, session_length=75)

        res = self.client.get(
            reverse("tutors:availability", kwargs={"pk": 1, "month": 12, "year": 2023})
        )
        self.assertContains(res, "60 minutes")

        res = self.client.get(
            reverse("tutors:availability", kwargs={"pk": 4, "month": 12, "year": 2023})
        )
        self.assertContains(res, "75 minutes")

    def test_correct_month_name_displayed_on_page(self):
        self._register_user("tutor1", student=False)
        tutor = Profile.objects.get(pk=1)
        self._create_service_objects(profile=tutor)

        res = self.client.get(
            reverse("tutors:availability", kwargs={"pk": 1, "month": 12, "year": 2023})
        )

        self.assertContains(res, "December")

    def test_availability_for_given_month_in_db_correctly_displayed(self):
        self._register_user("tutor1", student=False)
        tutor = Profile.objects.get(pk=1)
        self._create_service_objects(profile=tutor)
        service = Service.objects.get(pk=1)
        self._create_availiability_object(
            service=service, start=datetime(2023, 12, 17, 7, 0, tzinfo=timezone.utc)
        )
        self._create_availiability_object(
            service=service, start=datetime(2023, 12, 17, 8, 0, tzinfo=timezone.utc)
        )

        res = self.client.get(
            reverse("tutors:availability", kwargs={"pk": 1, "month": 12, "year": 2023})
        )

        self.assertContains(
            res,
            """<div class="popup-main-availabilites-availability popup-main-form box box-main adjacent-container">
                            <div class="popup-main-form-info adjacent-container"> 
                                <div class="popup-main-form-info-start">
                                    <div class="popup-main-form-info-start-top info-top">
                                        Start
                                    </div>
                                    <div class="popup-main-form-info-start-bottom info-bottom">
                                        <input type="time" class="popup-main-form-info-start-bottom-input time-input" id="popup-main-form-info-start-bottom-input-1" value="07:00" readonly="">
                                    </div> 
                                </div>
                                <div class="popup-main-form-info-end">
                                    <div class="popup-main-form-info-end-top info-top">
                                        End
                                    </div>
                                    <div class="popup-main-form-info-end-bottom info-bottom">
                                        <input type="time" class="popup-main-form-info-end-bottom-input time-input_readonly" value="08:00" readonly="">
                                    </div>
                                </div>
                            </div>
        
                            <div class="popup-main-availabilites-availability-delete popup-main-form-delete icon_green" id="popup-main-availabilites-availability-delete-1">
                                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-x-lg" viewBox="0 0 16 16">
                                    <path d="M2.146 2.854a.5.5 0 1 1 .708-.708L8 7.293l5.146-5.147a.5.5 0 0 1 .708.708L8.707 8l5.147 5.146a.5.5 0 0 1-.708.708L8 8.707l-5.146 5.147a.5.5 0 0 1-.708-.708L7.293 8 2.146 2.854Z"></path>
                                </svg>
                            </div>
                        </div>""",
            html=True,
        )
        self.assertContains(
            res,
            """<div class="popup-main-availabilites-availability popup-main-form box box-main adjacent-container">
                            <div class="popup-main-form-info adjacent-container"> 
                                <div class="popup-main-form-info-start">
                                    <div class="popup-main-form-info-start-top info-top">
                                        Start
                                    </div>
                                    <div class="popup-main-form-info-start-bottom info-bottom">
                                        <input type="time" class="popup-main-form-info-start-bottom-input time-input" id="popup-main-form-info-start-bottom-input-2" value="08:00" readonly="">
                                    </div> 
                                </div>
                                <div class="popup-main-form-info-end">
                                    <div class="popup-main-form-info-end-top info-top">
                                        End
                                    </div>
                                    <div class="popup-main-form-info-end-bottom info-bottom">
                                        <input type="time" class="popup-main-form-info-end-bottom-input time-input_readonly" value="09:00" readonly="">
                                    </div>
                                </div>
                            </div>
        
                            <div class="popup-main-availabilites-availability-delete popup-main-form-delete icon_green" id="popup-main-availabilites-availability-delete-2">
                                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-x-lg" viewBox="0 0 16 16">
                                    <path d="M2.146 2.854a.5.5 0 1 1 .708-.708L8 7.293l5.146-5.147a.5.5 0 0 1 .708.708L8.707 8l5.147 5.146a.5.5 0 0 1-.708.708L8 8.707l-5.146 5.147a.5.5 0 0 1-.708-.708L7.293 8 2.146 2.854Z"></path>
                                </svg>
                            </div>
                        </div>""",
            html=True,
        )

    def test_availability_for_differenet_month_in_db_not_displayed(self):
        self._register_user("tutor1", student=False)
        tutor = Profile.objects.get(pk=1)
        self._create_service_objects(profile=tutor)
        service = Service.objects.get(pk=1)
        self._create_availiability_object(
            service=service, start=datetime(2024, 1, 17, 7, 0, tzinfo=timezone.utc)
        )
        self._create_availiability_object(
            service=service, start=datetime(2024, 1, 17, 8, 0, tzinfo=timezone.utc)
        )

        res = self.client.get(
            reverse("tutors:availability", kwargs={"pk": 1, "month": 12, "year": 2023})
        )

        self.assertNotContains(
            res,
            """<div class="popup-main-availabilites-availability popup-main-form box box-main adjacent-container">
                            <div class="popup-main-form-info adjacent-container"> 
                                <div class="popup-main-form-info-start">
                                    <div class="popup-main-form-info-start-top info-top">
                                        Start
                                    </div>
                                    <div class="popup-main-form-info-start-bottom info-bottom">
                                        <input type="time" class="popup-main-form-info-start-bottom-input time-input" id="popup-main-form-info-start-bottom-input-1" value="07:00" readonly="">
                                    </div> 
                                </div>
                                <div class="popup-main-form-info-end">
                                    <div class="popup-main-form-info-end-top info-top">
                                        End
                                    </div>
                                    <div class="popup-main-form-info-end-bottom info-bottom">
                                        <input type="time" class="popup-main-form-info-end-bottom-input time-input_readonly" value="08:00" readonly="">
                                    </div>
                                </div>
                            </div>
        
                            <div class="popup-main-availabilites-availability-delete popup-main-form-delete icon_green" id="popup-main-availabilites-availability-delete-1">
                                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-x-lg" viewBox="0 0 16 16">
                                    <path d="M2.146 2.854a.5.5 0 1 1 .708-.708L8 7.293l5.146-5.147a.5.5 0 0 1 .708.708L8.707 8l5.147 5.146a.5.5 0 0 1-.708.708L8 8.707l-5.146 5.147a.5.5 0 0 1-.708-.708L7.293 8 2.146 2.854Z"></path>
                                </svg>
                            </div>
                        </div>""",
            html=True,
        )

        self.assertNotContains(
            res,
            """<div class="popup-main-availabilites-availability popup-main-form box box-main adjacent-container">
                            <div class="popup-main-form-info adjacent-container"> 
                                <div class="popup-main-form-info-start">
                                    <div class="popup-main-form-info-start-top info-top">
                                        Start
                                    </div>
                                    <div class="popup-main-form-info-start-bottom info-bottom">
                                        <input type="time" class="popup-main-form-info-start-bottom-input time-input" id="popup-main-form-info-start-bottom-input-2" value="08:00" readonly="">
                                    </div> 
                                </div>
                                <div class="popup-main-form-info-end">
                                    <div class="popup-main-form-info-end-top info-top">
                                        End
                                    </div>
                                    <div class="popup-main-form-info-end-bottom info-bottom">
                                        <input type="time" class="popup-main-form-info-end-bottom-input time-input_readonly" value="09:00" readonly="">
                                    </div>
                                </div>
                            </div>
        
                            <div class="popup-main-availabilites-availability-delete popup-main-form-delete icon_green" id="popup-main-availabilites-availability-delete-2">
                                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-x-lg" viewBox="0 0 16 16">
                                    <path d="M2.146 2.854a.5.5 0 1 1 .708-.708L8 7.293l5.146-5.147a.5.5 0 0 1 .708.708L8.707 8l5.147 5.146a.5.5 0 0 1-.708.708L8 8.707l-5.146 5.147a.5.5 0 0 1-.708-.708L7.293 8 2.146 2.854Z"></path>
                                </svg>
                            </div>
                        </div>""",
            html=True,
        )

    def test_availability_for_given_month_in_db_end_time_correctly_displayed(self):
        self._register_user("tutor1", student=False)
        tutor = Profile.objects.get(pk=1)
        self._create_service_objects(profile=tutor)
        self._create_service_object(profile=tutor, subject_pk=4, session_length=75)

        service = Service.objects.get(pk=4)
        self._create_availiability_object(
            service=service, start=datetime(2023, 12, 17, 7, 0, tzinfo=timezone.utc)
        )
        self._create_availiability_object(
            service=service, start=datetime(2023, 12, 17, 8, 30, tzinfo=timezone.utc)
        )

        res = self.client.get(
            reverse("tutors:availability", kwargs={"pk": 1, "month": 12, "year": 2023})
        )

        self.assertNotContains(
            res,
            """<div class="popup-main-availabilites-availability popup-main-form box box-main adjacent-container">
                            <div class="popup-main-form-info adjacent-container"> 
                                <div class="popup-main-form-info-start">
                                    <div class="popup-main-form-info-start-top info-top">
                                        Start
                                    </div>
                                    <div class="popup-main-form-info-start-bottom info-bottom">
                                        <input type="time" class="popup-main-form-info-start-bottom-input time-input" id="popup-main-form-info-start-bottom-input-1" value="07:00" readonly="">
                                    </div> 
                                </div>
                                <div class="popup-main-form-info-end">
                                    <div class="popup-main-form-info-end-top info-top">
                                        End
                                    </div>
                                    <div class="popup-main-form-info-end-bottom info-bottom">
                                        <input type="time" class="popup-main-form-info-end-bottom-input time-input_readonly" value="08:15" readonly="">
                                    </div>
                                </div>
                            </div>
        
                            <div class="popup-main-availabilites-availability-delete popup-main-form-delete icon_green" id="popup-main-availabilites-availability-delete-1">
                                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-x-lg" viewBox="0 0 16 16">
                                    <path d="M2.146 2.854a.5.5 0 1 1 .708-.708L8 7.293l5.146-5.147a.5.5 0 0 1 .708.708L8.707 8l5.147 5.146a.5.5 0 0 1-.708.708L8 8.707l-5.146 5.147a.5.5 0 0 1-.708-.708L7.293 8 2.146 2.854Z"></path>
                                </svg>
                            </div>
                        </div>""",
            html=True,
        )

        self.assertNotContains(
            res,
            """<div class="popup-main-availabilites-availability popup-main-form box box-main adjacent-container">
                            <div class="popup-main-form-info adjacent-container"> 
                                <div class="popup-main-form-info-start">
                                    <div class="popup-main-form-info-start-top info-top">
                                        Start
                                    </div>
                                    <div class="popup-main-form-info-start-bottom info-bottom">
                                        <input type="time" class="popup-main-form-info-start-bottom-input time-input" id="popup-main-form-info-start-bottom-input-2" value="08:30" readonly="">
                                    </div> 
                                </div>
                                <div class="popup-main-form-info-end">
                                    <div class="popup-main-form-info-end-top info-top">
                                        End
                                    </div>
                                    <div class="popup-main-form-info-end-bottom info-bottom">
                                        <input type="time" class="popup-main-form-info-end-bottom-input time-input_readonly" value="09:45" readonly="">
                                    </div>
                                </div>
                            </div>
        
                            <div class="popup-main-availabilites-availability-delete popup-main-form-delete icon_green" id="popup-main-availabilites-availability-delete-2">
                                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-x-lg" viewBox="0 0 16 16">
                                    <path d="M2.146 2.854a.5.5 0 1 1 .708-.708L8 7.293l5.146-5.147a.5.5 0 0 1 .708.708L8.707 8l5.147 5.146a.5.5 0 0 1-.708.708L8 8.707l-5.146 5.147a.5.5 0 0 1-.708-.708L7.293 8 2.146 2.854Z"></path>
                                </svg>
                            </div>
                        </div>""",
            html=True,
        )

    def test_currently_logged_in_user_not_the_tutor_user_redirected(self):
        self._register_user("tutor1", student=False)
        tutor = Profile.objects.get(pk=1)
        self._create_service_objects(profile=tutor)
        self._register_user("tutor2", student=False)
        self.client.login(username="tutor2", password="haslo123")

        res = self.client.get(
            reverse("tutors:availability", kwargs={"pk": 1, "month": 12, "year": 2023})
        )

        self.assertEqual(res.status_code, 403)
        self.assertContains(
            res,
            "You are not allowe to configure tutor's services!",
            status_code=403,
            html=True,
        )

    @freeze_time(NOW)
    def test_post_request_sent_availability_object_created(self):
        self._register_user("tutor1", student=False)
        tutor = Profile.objects.get(pk=1)
        self._create_service_objects(profile=tutor)

        res = self.client.post(
            reverse("tutors:availability_create"),
            data={
                "service": 1,
                "start": "2023-12-20 07:00",
            },
        )

        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(Availability.objects.all()), 1)

        availability = Availability.objects.get(pk=1)

        self.assertEqual(availability.service, Service.objects.get(pk=1))
        self.assertEqual(
            availability.start, datetime(2023, 12, 20, 7, 0, tzinfo=timezone.utc)
        )

    @freeze_time(NOW)
    def test_post_request_sent_availability_object_displayed_on_page(self):
        self._register_user("tutor1", student=False)
        tutor = Profile.objects.get(pk=1)
        self._create_service_objects(profile=tutor)

        self.client.post(
            reverse("tutors:availability_create"),
            data={
                "service": 1,
                "start": "2023-12-20 07:00",
            },
        )

        res = self.client.get(
            reverse("tutors:availability", kwargs={"pk": 1, "month": 12, "year": 2023})
        )

        self.assertContains(
            res,
            """<div class="popup-main-availabilites-availability popup-main-form box box-main adjacent-container">
                            <div class="popup-main-form-info adjacent-container"> 
                                <div class="popup-main-form-info-start">
                                    <div class="popup-main-form-info-start-top info-top">
                                        Start
                                    </div>
                                    <div class="popup-main-form-info-start-bottom info-bottom">
                                        <input type="time" class="popup-main-form-info-start-bottom-input time-input" id="popup-main-form-info-start-bottom-input-1" value="07:00" readonly="">
                                    </div> 
                                </div>
                                <div class="popup-main-form-info-end">
                                    <div class="popup-main-form-info-end-top info-top">
                                        End
                                    </div>
                                    <div class="popup-main-form-info-end-bottom info-bottom">
                                        <input type="time" class="popup-main-form-info-end-bottom-input time-input_readonly" value="08:00" readonly="">
                                    </div>
                                </div>
                            </div>
        
                            <div class="popup-main-availabilites-availability-delete popup-main-form-delete icon_green" id="popup-main-availabilites-availability-delete-1">
                                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-x-lg" viewBox="0 0 16 16">
                                    <path d="M2.146 2.854a.5.5 0 1 1 .708-.708L8 7.293l5.146-5.147a.5.5 0 0 1 .708.708L8.707 8l5.147 5.146a.5.5 0 0 1-.708.708L8 8.707l-5.146 5.147a.5.5 0 0 1-.708-.708L7.293 8 2.146 2.854Z"></path>
                                </svg>
                            </div>
                        </div>""",
            html=True,
        )

    def test_delete_request_sent_availability_object_deleted(self):
        self._register_user("tutor1", student=False)
        tutor = Profile.objects.get(pk=1)
        self._create_service_objects(profile=tutor)
        service = Service.objects.get(pk=1)
        self._create_availiability_object(
            service=service, start=datetime(2023, 12, 17, 7, 0, tzinfo=timezone.utc)
        )
        self._create_availiability_object(
            service=service, start=datetime(2023, 12, 17, 8, 0, tzinfo=timezone.utc)
        )

        self.client.delete(reverse("tutors:availability_delete", kwargs={"pk": 1}))

        self.assertEqual(len(Availability.objects.all()), 1)

    def test_delete_request_sent_availability_object_not_displayed_on_page(self):
        self._register_user("tutor1", student=False)
        tutor = Profile.objects.get(pk=1)
        self._create_service_objects(profile=tutor)
        service = Service.objects.get(pk=1)
        self._create_availiability_object(
            service=service, start=datetime(2023, 12, 17, 7, 0, tzinfo=timezone.utc)
        )
        self._create_availiability_object(
            service=service, start=datetime(2023, 12, 17, 8, 0, tzinfo=timezone.utc)
        )

        self.client.delete(reverse("tutors:availability_delete", kwargs={"pk": 1}))

        res = self.client.get(
            reverse("tutors:availability", kwargs={"pk": 1, "month": 12, "year": 2023})
        )

        self.assertNotContains(
            res,
            """<div class="popup-main-availabilites-availability popup-main-form box box-main adjacent-container">
                            <div class="popup-main-form-info adjacent-container"> 
                                <div class="popup-main-form-info-start">
                                    <div class="popup-main-form-info-start-top info-top">
                                        Start
                                    </div>
                                    <div class="popup-main-form-info-start-bottom info-bottom">
                                        <input type="time" class="popup-main-form-info-start-bottom-input time-input" id="popup-main-form-info-start-bottom-input-1" value="07:00" readonly="">
                                    </div> 
                                </div>
                                <div class="popup-main-form-info-end">
                                    <div class="popup-main-form-info-end-top info-top">
                                        End
                                    </div>
                                    <div class="popup-main-form-info-end-bottom info-bottom">
                                        <input type="time" class="popup-main-form-info-end-bottom-input time-input_readonly" value="08:00" readonly="">
                                    </div>
                                </div>
                            </div>
        
                            <div class="popup-main-availabilites-availability-delete popup-main-form-delete icon_green" id="popup-main-availabilites-availability-delete-1">
                                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-x-lg" viewBox="0 0 16 16">
                                    <path d="M2.146 2.854a.5.5 0 1 1 .708-.708L8 7.293l5.146-5.147a.5.5 0 0 1 .708.708L8.707 8l5.147 5.146a.5.5 0 0 1-.708.708L8 8.707l-5.146 5.147a.5.5 0 0 1-.708-.708L7.293 8 2.146 2.854Z"></path>
                                </svg>
                            </div>
                        </div>""",
            html=True,
        )

    @freeze_time(NOW)
    def test_post_request_sent_conflicting_availability_exists_error_message_returned(
        self,
    ):
        self._register_user("tutor1", student=False)
        tutor = Profile.objects.get(pk=1)
        self._create_service_objects(profile=tutor)

        service = Service.objects.get(pk=1)
        self._create_availiability_object(
            service=service, start=datetime(2023, 12, 20, 6, 30)
        )

        res_post = self.client.post(
            reverse("tutors:availability_create"),
            data={
                "service": 1,
                "start": "2023-12-20 07:00",
            },
        )

        self.assertEqual(res_post.status_code, 400)
        self.assertContains(
            res_post,
            "There is an Availability object with a conflicting time slot already in the database.",
            status_code=400,
        )

    @freeze_time(NOW)
    def test_post_request_sent_time_slot_falls_in_the_past_error_message_returned(self):
        self._register_user("tutor1", student=False)
        tutor = Profile.objects.get(pk=1)
        self._create_service_objects(profile=tutor)

        service = Service.objects.get(pk=1)
        self._create_availiability_object(
            service=service, start=datetime(2023, 12, 20, 6, 30)
        )

        res_post = self.client.post(
            reverse("tutors:availability_create"),
            data={
                "service": 1,
                "start": "2023-12-10 07:00",
            },
        )

        self.assertEqual(res_post.status_code, 400)
        self.assertContains(
            res_post,
            "Given time slot falls in the past. Please input valid start time.",
            status_code=400,
        )
