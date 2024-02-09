"""Tests for the `learning_tutor` page."""


from datetime import datetime, timedelta

from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.timezone import now
from freezegun import freeze_time
from parameterized import parameterized

from profiles.models import Profile
from subscriptions.models import ServiceSubscriptionList, Subscription
from tutors.models import Service, Subject
from utils.testing import NOW, TestCaseSubscriptionUtils


class TestLearningTutorView(TestCaseSubscriptionUtils):
    """Tests for the functionality of displaying and/or adding Subscription, ServiceSubscriptionList and Appointment objects."""

    def setUp(self):
        """Initial database setup."""
        super().setUp()
        tutor = Profile.objects.get(user__username="tutor1")
        student1 = Profile.objects.get(user__username="student1")
        subject1 = Subject.objects.get(pk=1)
        student2 = Profile.objects.get(user__username="student2")
        subject2 = Subject.objects.get(pk=2)
        subscription1 = self._create_subscription_object(
            tutor=tutor, student=student1, subject=subject1
        )
        subscription2 = self._create_subscription_object(
            tutor=tutor, student=student2, subject=subject2
        )

        service = Service.objects.get(pk=1)
        self.service_subscription_list = self._create_servicesubscriptionlist_object(
            subscription=subscription1,
            service=service,
        )

    @parameterized.expand(
        [("tutor1", "haslo123"), ("student1", "haslo123"), ("tutor2", "haslo123")]
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
            ("GET", "student1", "haslo123"),
            ("GET", "tutor2", "haslo123"),
            ("POST", "student1", "haslo123"),
            ("POST", "tutor2", "haslo123"),
        ]
    )
    def test_user_is_not_related_tutor_warning_page_displayed(
        self, request_type, username, password
    ):
        self.client.login(username=username, password=password)
        url = reverse("subscriptions:learning_tutor", kwargs={"subscription_id": 1})
        res = self.client.get(url) if request_type == "GET" else self.client.post(url)

        self.assertEquals(res.status_code, 403)
        self.assertContains(
            res, "You are not allowed to access this page.", status_code=403
        )

    def test_user_is_related_tutor_get_request_page_displayed(self):
        self.client.login(username="tutor1", password="haslo123")
        res = self.client.get(
            reverse("subscriptions:learning_tutor", kwargs={"subscription_id": 1})
        )

        self.assertEquals(res.status_code, 200)

    def test_user_is_related_tutor_get_request_subscribed_students_displayed(self):
        student1, student2 = User.objects.get(username="student1"), User.objects.get(
            username="student2"
        )

        student1.first_name, student1.last_name = "John", "Smith"
        student2.first_name, student2.last_name = "Jane", "Smith"

        student1.save()
        student2.save()

        self.client.login(username="tutor1", password="haslo123")
        res = self.client.get(
            reverse("subscriptions:learning_tutor", kwargs={"subscription_id": 1})
        )

        self.assertContains(
            res,
            """<div class="learnign-left-assigned-main-student-name bolded">
                                    John Smith                        
                                </div>""",
            html=True,
        )
        self.assertContains(
            res,
            f"""<div class="learnign-left-assigned-main-student-name link-container">
                                    <a href="{reverse("subscriptions:learning_tutor", kwargs={"subscription_id": 2})}">
                                        Jane Smith
                                    </a>
                                </div>""",
            html=True,
        )

    def test_user_is_related_tutor_get_request_correct_services_displayed(self):
        self.client.login(username="tutor1", password="haslo123")
        res = self.client.get(
            reverse("subscriptions:learning_tutor", kwargs={"subscription_id": 1})
        )

        self.assertContains(res, '<option value="1">Math, 1 hour</option>', html=True)
        self.assertContains(res, '<option value="3">Math, 10 hours</option>', html=True)

    def test_user_is_related_tutor_get_request_correct_subject_displayed(self):
        self.client.login(username="tutor1", password="haslo123")
        res = self.client.get(
            reverse("subscriptions:learning_tutor", kwargs={"subscription_id": 1})
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

    def test_user_is_related_tutor_get_request_correct_number_of_total_and_available_hours_displayed_no_appointment(
        self,
    ):
        self._create_servicesubscriptionlist_object(
            subscription=Subscription.objects.get(pk=1),
            service=Service.objects.get(pk=3),
        )

        self.client.login(username="tutor1", password="haslo123")
        res = self.client.get(
            reverse("subscriptions:learning_tutor", kwargs={"subscription_id": 1})
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

    def test_user_is_related_tutor_get_request_correct_number_of_total_and_available_hours_displayed_appointments_created(
        self,
    ):
        self._create_appointment_object(
            service_subscription_list=self.service_subscription_list
        )
        self._create_servicesubscriptionlist_object(
            subscription=Subscription.objects.get(pk=1),
            service=Service.objects.get(pk=3),
        )

        self.client.login(username="tutor1", password="haslo123")
        res = self.client.get(
            reverse("subscriptions:learning_tutor", kwargs={"subscription_id": 1})
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
    def test_user_is_related_tutor_get_request_related_appointments_displayed(self):
        appointment = self._create_appointment_object(
            service_subscription_list=self.service_subscription_list
        )
        lesson_title = "Lesson's title"
        appointment.lesson_info.title = lesson_title
        yesterday = now() - timedelta(days=1)
        appointment.lesson_info.date = datetime(
            year=yesterday.year, month=yesterday.month, day=yesterday.day, hour=12
        )
        appointment.lesson_info.save()

        self.client.login(username="tutor1", password="haslo123")
        res = self.client.get(
            reverse("subscriptions:learning_tutor", kwargs={"subscription_id": 1})
        )

        display_lesson_url = reverse(
            "lessons:lesson_display_tutor", kwargs={"pk": appointment.lesson_info.pk}
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
                            </div>  
                            <div class="learning-right-sessions-session-bottom">
                                12. Dec 2023, 12:00 - 13:00
                            </div>
                        </div>""",
            html=True,
        )

    @freeze_time(NOW)
    def test_user_is_related_tutor_get_request_appointment_in_past_no_delete_btn_displayed(
        self,
    ):
        appointment = self._create_appointment_object(
            service_subscription_list=self.service_subscription_list
        )
        lesson_title = "Lesson's title"
        appointment.lesson_info.title = lesson_title
        yesterday = now() - timedelta(days=1)
        appointment.lesson_info.date = datetime(
            year=yesterday.year, month=yesterday.month, day=yesterday.day, hour=12
        )
        appointment.lesson_info.save()

        self.client.login(username="tutor1", password="haslo123")
        res = self.client.get(
            reverse("subscriptions:learning_tutor", kwargs={"subscription_id": 1})
        )

        display_lesson_url = reverse(
            "lessons:lesson_display_tutor", kwargs={"pk": appointment.lesson_info.pk}
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
                            </div>  
                            <div class="learning-right-sessions-session-bottom">
                                12. Dec 2023, 12:00 - 13:00
                            </div>
                        </div>""",
            html=True,
        )
        delete_appointment_url = reverse(
            "subscriptions:appointment_delete", kwargs={"pk": appointment.pk}
        )
        self.assertNotContains(
            res,
            f"""<div class="learning-right-sessions-session-top-delete icon_green link-container">
                                        <a href="{delete_appointment_url}">
                                            <svg xmlns="http://www.w3.org/2000/svg" fill="currentColor" class="bi bi-x-lg" viewBox="0 0 16 16">
                                                <path d="M2.146 2.854a.5.5 0 1 1 .708-.708L8 7.293l5.146-5.147a.5.5 0 0 1 .708.708L8.707 8l5.147 5.146a.5.5 0 0 1-.708.708L8 8.707l-5.146 5.147a.5.5 0 0 1-.708-.708L7.293 8z"></path>
                                            </svg>
                                        </a>
                                    </div>""",
            html=True,
        )

    @freeze_time(NOW)
    def test_user_is_related_tutor_get_request_appointment_in_future_delete_btn_displayed(
        self,
    ):
        appointment = self._create_appointment_object(
            service_subscription_list=self.service_subscription_list
        )
        lesson_title = "Lesson's title"
        appointment.lesson_info.title = lesson_title
        tomorrow = now() + timedelta(days=1)
        appointment.lesson_info.date = datetime(
            year=tomorrow.year, month=tomorrow.month, day=tomorrow.day, hour=12
        )
        appointment.lesson_info.save()

        self.client.login(username="tutor1", password="haslo123")
        res = self.client.get(
            reverse("subscriptions:learning_tutor", kwargs={"subscription_id": 1})
        )

        display_lesson_url = reverse(
            "lessons:lesson_display_tutor", kwargs={"pk": appointment.lesson_info.pk}
        )
        delete_appointment_url = reverse(
            "subscriptions:appointment_delete", kwargs={"pk": appointment.pk}
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
                                    <a href="{delete_appointment_url}">
                                        <svg xmlns="http://www.w3.org/2000/svg" fill="currentColor" class="bi bi-x-lg" viewBox="0 0 16 16">
                                            <path d="M2.146 2.854a.5.5 0 1 1 .708-.708L8 7.293l5.146-5.147a.5.5 0 0 1 .708.708L8.707 8l5.147 5.146a.5.5 0 0 1-.708.708L8 8.707l-5.146 5.147a.5.5 0 0 1-.708-.708L7.293 8z"></path>
                                        </svg>
                                    </a>
                                </div>
                            </div>  
                            <div class="learning-right-sessions-session-bottom">
                                14. Dec 2023, 12:00 - 13:00
                            </div>
                        </div>""",
            html=True,
        )

    def test_user_is_related_tutor_post_request_servicesubscriptionlist_object_created(
        self,
    ):
        self.client.login(username="tutor1", password="haslo123")
        res = self.client.post(
            path=reverse("subscriptions:learning_tutor", kwargs={"subscription_id": 1}),
            data={"service": 3},
        )
        self.assertEqual(res.status_code, 302)
        self.assertEqual(len(ServiceSubscriptionList.objects.all()), 2)

    def test_user_is_related_tutor_post_request_user_correctly_redirected(self):
        self.client.login(username="tutor1", password="haslo123")
        res = self.client.post(
            path=reverse("subscriptions:learning_tutor", kwargs={"subscription_id": 1}),
            data={"service": 3},
            follow=True,
        )
        self.assertRedirects(
            res, reverse("subscriptions:learning_tutor", kwargs={"subscription_id": 1})
        )
        self.assertEqual(len(ServiceSubscriptionList.objects.all()), 2)
