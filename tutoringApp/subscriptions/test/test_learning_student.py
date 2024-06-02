"""Tests for the `learning_student` page."""

from datetime import datetime, timedelta, timezone

from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.timezone import now
from freezegun import freeze_time
from parameterized import parameterized

from profiles.models import Profile
from subscriptions.models import Subscription
from tutors.models import Service, Subject
from utils.testing import NOW, TestCaseSubscriptionUtils


class TestLearningStudentView(TestCaseSubscriptionUtils):
    """Tests for the functionality of displaying Subscription and Appointment objects."""

    def setUp(self):
        """Initial database setup."""
        super().setUp()
        student = Profile.objects.get(user__username="student1")

        tutor1 = Profile.objects.get(user__username="tutor1")
        subject1 = Subject.objects.get(pk=1)
        self.subscription1 = self._create_subscription_object(
            tutor=tutor1, student=student, subject=subject1
        )
        service = Service.objects.get(pk=1)
        self.service_subscription_list = self._create_servicesubscriptionlist_object(
            subscription=self.subscription1,
            service=service,
        )

        tutor2 = Profile.objects.get(user__username="tutor2")
        subject2 = Subject.objects.get(pk=2)
        self._create_service_object(profile=tutor2, subject_pk=subject2.pk)
        self.subscription2 = self._create_subscription_object(
            tutor=tutor2, student=student, subject=subject2
        )

    @parameterized.expand(
        [("student1", "haslo123"), ("tutor1", "haslo123"), ("tutor2", "haslo123")]
    )
    def test_subscription_does_not_exist_exception_raised(self, username, password):
        self.client.login(username=username, password=password)
        subscription = Subscription.objects.get(pk=1)
        subscription.delete()

        self.assertRaises(
            Subscription.DoesNotExist,
            self.client.get,
            reverse("subscriptions:learning_tutor", kwargs={"subscription_id": 1}),
        )

    @parameterized.expand(
        [
            ("student2", "haslo123"),
            ("tutor2", "haslo123"),
        ]
    )
    def test_user_is_not_related_student_warning_page_displayed(
        self, username, password
    ):
        self.client.login(username=username, password=password)
        res = self.client.get(
            reverse("subscriptions:learning_student", kwargs={"subscription_id": 1})
        )

        self.assertEquals(res.status_code, 403)
        self.assertContains(
            res, "You are not allowed to access this page.", status_code=403
        )

    def test_user_is_related_student_get_request_page_displayed(self):
        self.client.login(username="student1", password="haslo123")
        res = self.client.get(
            reverse("subscriptions:learning_student", kwargs={"subscription_id": 1})
        )

        self.assertEquals(res.status_code, 200)

    def test_user_is_related_student_all_tutors_displayed(self):
        tutor1, tutor2 = User.objects.get(username="tutor1"), User.objects.get(
            username="tutor2"
        )

        tutor1.first_name, tutor1.last_name = "John", "Smith"
        tutor2.first_name, tutor2.last_name = "Jane", "Smith"

        tutor1.save()
        tutor2.save()

        self.client.login(username="student1", password="haslo123")
        res = self.client.get(
            reverse("subscriptions:learning_student", kwargs={"subscription_id": 1})
        )

        self.assertContains(
            res,
            """<div class="learnign-left-tutors-main-tutor adjacent-container">
                            <div class="learnign-left-tutors-main-tutor-name bolded">
                                John Smith                        
                            </div>
                        <div class="learnign-left-tutors-main-tutor-subject info-bottom">
                            Math
                        </div>
                    </div>""",
            html=True,
        )
        self.assertContains(
            res,
            f"""<div class="learnign-left-tutors-main-tutor adjacent-container"> 
                            <div class="learnign-left-tutors-main-tutor-name link-container">
                                <a href="{reverse("subscriptions:learning_student", kwargs={"subscription_id": 2})}">
                                    Jane Smith
                                </a>
                            </div>
                        <div class="learnign-left-tutors-main-tutor-subject info-bottom">
                            English
                        </div>
                    </div>""",
            html=True,
        )

    def test_user_is_related_student_correct_subject_displayed(self):
        self.client.login(username="student1", password="haslo123")
        res = self.client.get(
            reverse("subscriptions:learning_student", kwargs={"subscription_id": 1})
        )

        self.assertContains(
            res,
            """<td class="learning-right-summary-main-table-cell">
                            <div class="learning-right-summary-main-table-cell-top">
                                Subject
                            </div>
                            <div class="learning-right-summary-main-table-cell-bottom">
                                Math
                            </div>
                        </td>""",
            html=True,
        )

    def test_user_is_related_student_correct_number_of_total_and_available_hours_displayed_no_appointment(
        self,
    ):
        self._create_servicesubscriptionlist_object(
            subscription=Subscription.objects.get(pk=1),
            service=Service.objects.get(pk=3),
        )

        self.client.login(username="student1", password="haslo123")
        res = self.client.get(
            reverse("subscriptions:learning_student", kwargs={"subscription_id": 1})
        )

        self.assertContains(
            res,
            """<td class="learning-right-summary-main-table-cell">
                            <div class="learning-right-summary-main-table-cell-top">
                                Total number of hours
                            </div>
                            <div class="learning-right-summary-main-table-cell-bottom">
                                0
                            </div>
                        </td>""",
            html=True,
        )
        self.assertContains(
            res,
            """<td class="learning-right-summary-main-table-cell">
                            <div class="learning-right-summary-main-table-cell-top">
                                Hours left 
                            </div>
                            <div class="learning-right-summary-main-table-cell-bottom">
                                11
                            </div>
                        </td>""",
            html=True,
        )

    def test_user_is_related_student_correct_number_of_total_and_available_hours_displayed_appointments_created(
        self,
    ):
        self._create_appointment_object(
            service_subscription_list=self.service_subscription_list
        )
        self._create_servicesubscriptionlist_object(
            subscription=Subscription.objects.get(pk=1),
            service=Service.objects.get(pk=3),
        )

        self.client.login(username="student1", password="haslo123")
        res = self.client.get(
            reverse("subscriptions:learning_student", kwargs={"subscription_id": 1})
        )

        self.assertContains(
            res,
            """<td class="learning-right-summary-main-table-cell">
                            <div class="learning-right-summary-main-table-cell-top">
                                Total number of hours
                            </div>
                            <div class="learning-right-summary-main-table-cell-bottom">
                                1
                            </div>
                        </td>""",
            html=True,
        )
        self.assertContains(
            res,
            """<td class="learning-right-summary-main-table-cell">
                            <div class="learning-right-summary-main-table-cell-top">
                                Hours left 
                            </div>
                            <div class="learning-right-summary-main-table-cell-bottom">
                                10
                            </div>
                        </td>""",
            html=True,
        )

    @freeze_time(NOW)
    def test_user_is_related_student_related_appointments_displayed(self):
        appointment = self._create_appointment_object(
            service_subscription_list=self.service_subscription_list
        )
        lesson_title = "Lesson's title"
        appointment.lesson_info.title = lesson_title
        tomorrow = now() + timedelta(days=1)
        appointment.lesson_info.date = datetime(
            year=tomorrow.year, month=tomorrow.month, day=tomorrow.day, hour=12, tzinfo=timezone.utc
        )
        appointment.lesson_info.save()

        self.client.login(username="student1", password="haslo123")
        res = self.client.get(
            reverse("subscriptions:learning_student", kwargs={"subscription_id": 1})
        )

        display_lesson_url = reverse(
            "lessons:lesson_display_student", kwargs={"pk": appointment.lesson_info.pk}
        )
        self.assertContains(
            res,
            f"""<div class="learning-right-sessions-session">
                        <div class="learning-right-sessions-session-top">
                            <div class="learning-right-sessions-session-top-name">
                                <a href="{display_lesson_url}">
                                    {lesson_title}
                                </a>
                            </div>
                            <div class="learning-right-sessions-session-top-delete icon_green link-container">
                            </div>
                        </div>  
                        <div class="learning-right-sessions-session-bottom">
                            14. Dec 2023, 12:00 - 13:00
                        </div>
                    </div>""",
            html=True,
        )
