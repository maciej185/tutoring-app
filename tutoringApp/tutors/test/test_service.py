"""Test for service configuration views."""
from django.urls import reverse

from profiles.models import Profile
from tutors.models import Service, Subject
from utils.testing import TestCaseServiceUtils


class TestAvailabilityInputView(TestCaseServiceUtils):
    """Tests for the service configuration page."""

    def test_service_objects_in_db_correctly_displayed(self):
        self._register_user("tutor1", student=False)
        tutor = Profile.objects.get(pk=1)
        self._create_service_objects(profile=tutor)
        self._create_service_object(
            profile=tutor, subject_pk=3, number_of_hours=10, is_default=False
        )
        self._create_service_object(
            profile=tutor, subject_pk=4, number_of_hours=10, is_default=False
        )

        res = self.client.get(reverse("tutors:services", kwargs={"pk": 1}))

        self.assertContains(
            res,
            '<input type="hidden" name="service_set-0-id" value="1" id="id_service_set-0-id">',
            html=True,
        )
        self.assertContains(
            res,
            '<input type="hidden" name="service_set-1-id" value="2" id="id_service_set-1-id">',
            html=True,
        )
        self.assertContains(
            res,
            '<input type="hidden" name="service_set-2-id" value="3" id="id_service_set-2-id">',
            html=True,
        )
        self.assertContains(
            res,
            '<input type="hidden" name="service_set-3-id" value="4" id="id_service_set-3-id">',
            html=True,
        )
        self.assertContains(
            res,
            '<input type="hidden" name="service_set-4-id" value="5" id="id_service_set-4-id">',
            html=True,
        )

    def test_correct_form_data_service_object_updated(self):
        self._register_user("tutor1", student=False)
        tutor = Profile.objects.get(pk=1)
        self._create_service_objects(profile=tutor)
        self._create_service_object(
            profile=tutor, subject_pk=1, number_of_hours=10, is_default=False
        )
        self._create_service_object(
            profile=tutor, subject_pk=2, number_of_hours=10, is_default=False
        )

        self.client.post(
            reverse("tutors:services", kwargs={"pk": 1}),
            {
                "service_set-TOTAL_FORMS": 6,
                "service_set-INITIAL_FORMS": 5,
                "service_set-MIN_NUM_FORMS": 0,
                "service_set-0-id": 1,
                "service_set-0-tutor": 1,
                "service_set-0-subject": 1,
                "service_set-0-session_length": 75,
                "service_set-0-number_of_hours": 1,
                "service_set-0-price_per_hour": 100,
                "service_set-1-id": 2,
                "service_set-1-tutor": 1,
                "service_set-1-subject": 2,
                "service_set-1-session_length": 60,
                "service_set-1-number_of_hours": 1,
                "service_set-1-price_per_hour": 120,
                "service_set-2-id": 3,
                "service_set-2-tutor": 1,
                "service_set-2-subject": 1,
                "service_set-2-session_length": 60,
                "service_set-2-number_of_hours": 10,
                "service_set-2-price_per_hour": 80,
                "service_set-3-id": 4,
                "service_set-3-tutor": 1,
                "service_set-3-subject": 1,
                "service_set-3-session_length": 60,
                "service_set-3-number_of_hours": 10,
                "service_set-3-price_per_hour": 100,
                "service_set-4-id": 5,
                "service_set-4-tutor": 1,
                "service_set-4-subject": 2,
                "service_set-4-session_length": 60,
                "service_set-4-number_of_hours": 10,
                "service_set-4-price_per_hour": 100,
                "service_set-5-id": "",
                "service_set-5-tutor": 1,
                "service_set-5-subject": "",
                "service_set-5-session_length": 60,
                "service_set-5-number_of_hours": 1,
                "service_set-5-price_per_hour": "",
            },
        )
        service = Service.objects.get(pk=1)
        self.assertEqual(service.session_length, 75)

    def test_correct_form_data_service_object_created(self):
        self._register_user("tutor1", student=False)
        tutor = Profile.objects.get(pk=1)
        self._create_service_objects(profile=tutor)
        self._create_service_object(
            profile=tutor, subject_pk=1, number_of_hours=10, is_default=False
        )
        self._create_service_object(
            profile=tutor, subject_pk=2, number_of_hours=10, is_default=False
        )

        self.assertEqual(len(Service.objects.all()), 5)
        self.client.post(
            reverse("tutors:services", kwargs={"pk": 1}),
            {
                "service_set-TOTAL_FORMS": 6,
                "service_set-INITIAL_FORMS": 5,
                "service_set-MIN_NUM_FORMS": 0,
                "service_set-0-id": 1,
                "service_set-0-tutor": 1,
                "service_set-0-subject": 1,
                "service_set-0-session_length": 75,
                "service_set-0-number_of_hours": 1,
                "service_set-0-price_per_hour": 100,
                "service_set-1-id": 2,
                "service_set-1-tutor": 1,
                "service_set-1-subject": 2,
                "service_set-1-session_length": 60,
                "service_set-1-number_of_hours": 1,
                "service_set-1-price_per_hour": 120,
                "service_set-2-id": 3,
                "service_set-2-tutor": 1,
                "service_set-2-subject": 1,
                "service_set-2-session_length": 60,
                "service_set-2-number_of_hours": 10,
                "service_set-2-price_per_hour": 80,
                "service_set-3-id": 4,
                "service_set-3-tutor": 1,
                "service_set-3-subject": 1,
                "service_set-3-session_length": 60,
                "service_set-3-number_of_hours": 10,
                "service_set-3-price_per_hour": 100,
                "service_set-4-id": 5,
                "service_set-4-tutor": 1,
                "service_set-4-subject": 2,
                "service_set-4-session_length": 60,
                "service_set-4-number_of_hours": 10,
                "service_set-4-price_per_hour": 100,
                "service_set-5-id": "",
                "service_set-5-tutor": 1,
                "service_set-5-subject": 2,
                "service_set-5-session_length": 90,
                "service_set-5-number_of_hours": 15,
                "service_set-5-price_per_hour": 75,
            },
        )
        self.assertEqual(len(Service.objects.all()), 6)
        service = Service.objects.get(pk=6)
        self.assertEqual(service.subject, Subject.objects.get(pk=2))
        self.assertEqual(service.session_length, 90)
        self.assertEqual(service.number_of_hours, 15)
        self.assertEqual(service.price_per_hour, 75)

    def test_correct_form_data_already_exisiting_object_updated_and_new_one_created(
        self,
    ):
        self._register_user("tutor1", student=False)
        tutor = Profile.objects.get(pk=1)
        self._create_service_objects(profile=tutor)
        self._create_service_object(
            profile=tutor, subject_pk=1, number_of_hours=10, is_default=False
        )
        self._create_service_object(
            profile=tutor, subject_pk=2, number_of_hours=10, is_default=False
        )

        self.assertEqual(len(Service.objects.all()), 5)
        service3 = Service.objects.get(pk=3)
        self.assertEqual(service3.number_of_hours, 10)

        self.client.post(
            reverse("tutors:services", kwargs={"pk": 1}),
            {
                "service_set-TOTAL_FORMS": 6,
                "service_set-INITIAL_FORMS": 5,
                "service_set-MIN_NUM_FORMS": 0,
                "service_set-0-id": 1,
                "service_set-0-tutor": 1,
                "service_set-0-subject": 1,
                "service_set-0-session_length": 75,
                "service_set-0-number_of_hours": 1,
                "service_set-0-price_per_hour": 100,
                "service_set-1-id": 2,
                "service_set-1-tutor": 1,
                "service_set-1-subject": 2,
                "service_set-1-session_length": 60,
                "service_set-1-number_of_hours": 1,
                "service_set-1-price_per_hour": 120,
                "service_set-2-id": 3,
                "service_set-2-tutor": 1,
                "service_set-2-subject": 1,
                "service_set-2-session_length": 60,
                "service_set-2-number_of_hours": 20,
                "service_set-2-price_per_hour": 80,
                "service_set-3-id": 4,
                "service_set-3-tutor": 1,
                "service_set-3-subject": 1,
                "service_set-3-session_length": 60,
                "service_set-3-number_of_hours": 10,
                "service_set-3-price_per_hour": 100,
                "service_set-4-id": 5,
                "service_set-4-tutor": 1,
                "service_set-4-subject": 2,
                "service_set-4-session_length": 60,
                "service_set-4-number_of_hours": 10,
                "service_set-4-price_per_hour": 100,
                "service_set-5-id": "",
                "service_set-5-tutor": 1,
                "service_set-5-subject": 2,
                "service_set-5-session_length": 90,
                "service_set-5-number_of_hours": 15,
                "service_set-5-price_per_hour": 75,
            },
        )
        self.assertEqual(len(Service.objects.all()), 6)
        service = Service.objects.get(pk=6)
        self.assertEqual(service.subject, Subject.objects.get(pk=2))
        self.assertEqual(service.session_length, 90)
        self.assertEqual(service.number_of_hours, 15)
        self.assertEqual(service.price_per_hour, 75)

        service3.refresh_from_db()
        self.assertEqual(service3.number_of_hours, 20)

    def test_incorrect_form_data_new_service_object_not_created(self):
        self._register_user("tutor1", student=False)
        tutor = Profile.objects.get(pk=1)
        self._create_service_objects(profile=tutor)
        self._create_service_object(
            profile=tutor, subject_pk=1, number_of_hours=10, is_default=False
        )
        self._create_service_object(
            profile=tutor, subject_pk=2, number_of_hours=10, is_default=False
        )

        self.assertEqual(len(Service.objects.all()), 5)

        self.client.post(
            reverse("tutors:services", kwargs={"pk": 1}),
            {
                "service_set-TOTAL_FORMS": 6,
                "service_set-INITIAL_FORMS": 5,
                "service_set-MIN_NUM_FORMS": 0,
                "service_set-0-id": 1,
                "service_set-0-tutor": 1,
                "service_set-0-subject": 1,
                "service_set-0-session_length": 75,
                "service_set-0-number_of_hours": 1,
                "service_set-0-price_per_hour": 100,
                "service_set-1-id": 2,
                "service_set-1-tutor": 1,
                "service_set-1-subject": 2,
                "service_set-1-session_length": 60,
                "service_set-1-number_of_hours": 1,
                "service_set-1-price_per_hour": 120,
                "service_set-2-id": 3,
                "service_set-2-tutor": 1,
                "service_set-2-subject": 1,
                "service_set-2-session_length": 60,
                "service_set-2-number_of_hours": 10,
                "service_set-2-price_per_hour": 80,
                "service_set-3-id": 4,
                "service_set-3-tutor": 1,
                "service_set-3-subject": 1,
                "service_set-3-session_length": 60,
                "service_set-3-number_of_hours": 10,
                "service_set-3-price_per_hour": 100,
                "service_set-4-id": 5,
                "service_set-4-tutor": 1,
                "service_set-4-subject": 2,
                "service_set-4-session_length": 60,
                "service_set-4-number_of_hours": 10,
                "service_set-4-price_per_hour": 100,
                "service_set-5-id": "",
                "service_set-5-tutor": 1,
                "service_set-5-subject": 2,
                "service_set-5-session_length": 90,
                "service_set-5-number_of_hours": 15,
                "service_set-5-price_per_hour": "",
            },
        )
        self.assertEqual(len(Service.objects.all()), 5)

    def test_incorrect_form_data_message_displayed(self):
        self._register_user("tutor1", student=False)
        tutor = Profile.objects.get(pk=1)
        self._create_service_objects(profile=tutor)
        self._create_service_object(
            profile=tutor, subject_pk=1, number_of_hours=10, is_default=False
        )
        self._create_service_object(
            profile=tutor, subject_pk=2, number_of_hours=10, is_default=False
        )

        res = self.client.post(
            reverse("tutors:services", kwargs={"pk": 1}),
            {
                "service_set-TOTAL_FORMS": 6,
                "service_set-INITIAL_FORMS": 5,
                "service_set-MIN_NUM_FORMS": 0,
                "service_set-0-id": 1,
                "service_set-0-tutor": 1,
                "service_set-0-subject": 1,
                "service_set-0-session_length": 75,
                "service_set-0-number_of_hours": 1,
                "service_set-0-price_per_hour": 100,
                "service_set-1-id": 2,
                "service_set-1-tutor": 1,
                "service_set-1-subject": 2,
                "service_set-1-session_length": 60,
                "service_set-1-number_of_hours": 1,
                "service_set-1-price_per_hour": 120,
                "service_set-2-id": 3,
                "service_set-2-tutor": 1,
                "service_set-2-subject": 1,
                "service_set-2-session_length": 60,
                "service_set-2-number_of_hours": 10,
                "service_set-2-price_per_hour": 80,
                "service_set-3-id": 4,
                "service_set-3-tutor": 1,
                "service_set-3-subject": 1,
                "service_set-3-session_length": 60,
                "service_set-3-number_of_hours": 10,
                "service_set-3-price_per_hour": 100,
                "service_set-4-id": 5,
                "service_set-4-tutor": 1,
                "service_set-4-subject": 2,
                "service_set-4-session_length": 60,
                "service_set-4-number_of_hours": 10,
                "service_set-4-price_per_hour": 100,
                "service_set-5-id": "",
                "service_set-5-tutor": 1,
                "service_set-5-subject": 2,
                "service_set-5-session_length": 90,
                "service_set-5-number_of_hours": 15,
                "service_set-5-price_per_hour": "",
            },
            follow=True,
        )

        self.assertContains(res, "This field is required.")

    def test_attempt_to_delete_service_user_is_related_tutor_object_deleted_from_db(
        self,
    ):
        self._register_user("tutor1", student=False)
        tutor = Profile.objects.get(pk=1)
        self._create_service_objects(profile=tutor)

        self.assertEqual(len(Service.objects.all()), 3)

        self.client.get(
            reverse("tutors:service_delete", kwargs={"service_id": 1}), follow=True
        )

        self.assertEqual(len(Service.objects.all()), 2)

    def test_attempt_to_delete_service_user_is_related_tutor_object_not_displayed_on_page(
        self,
    ):
        self._register_user("tutor1", student=False)
        tutor = Profile.objects.get(pk=1)
        self._create_service_objects(profile=tutor)

        self.client.get(
            reverse("tutors:service_delete", kwargs={"service_id": 2}), follow=True
        )

        res = self.client.get(reverse("tutors:services", kwargs={"pk": 1}))

        self.assertContains(
            res,
            '<input type="hidden" name="service_set-0-id" value="1" id="id_service_set-0-id">',
            html=True,
        )
        self.assertContains(
            res,
            '<input type="hidden" name="service_set-1-id" value="3" id="id_service_set-1-id">',
            html=True,
        )

    def test_attempt_to_delete_service_user_not_related_tutor_correctly_redirected(
        self,
    ):
        self._register_user("tutor1", student=False)
        tutor = Profile.objects.get(pk=1)
        self._create_service_objects(profile=tutor)
        self._register_user("tutor2", student=False)
        self.client.login(username="tutor2", password="haslo123")

        res = self.client.get(
            reverse("tutors:service_delete", kwargs={"service_id": 2}), follow=True
        )

        self.assertEqual(res.status_code, 403)
        self.assertContains(
            res,
            "You are not allowed to delete tutor's services!",
            status_code=403,
            html=True,
        )

    def test_attempt_to_configure_services_user_not_related_tutor_conrrectly_redirected(
        self,
    ):
        self._register_user("tutor1", student=False)
        tutor = Profile.objects.get(pk=1)
        self._create_service_objects(profile=tutor)
        self._register_user("tutor2", student=False)
        self.client.login(username="tutor2", password="haslo123")

        res = self.client.get(reverse("tutors:services", kwargs={"pk": 1}))

        self.assertEqual(res.status_code, 403)
        self.assertContains(
            res,
            "You are not allowed to configure tutor's services!",
            status_code=403,
            html=True,
        )
