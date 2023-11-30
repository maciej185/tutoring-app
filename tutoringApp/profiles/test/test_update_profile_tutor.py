import re
from datetime import date
from pathlib import Path

from django.conf import settings
from django.contrib.auth.models import User
from django.urls import reverse
from parameterized import parameterized

from profiles.models import (
    Education,
    Language,
    Profile,
    ProfileLanguageList,
    School,
    Service,
    Subject,
)
from utils.testing import TestCaseUserUtils

CORRECT_UPDATE_TUTOR_PROFILE_DATA = lambda user: {
    "first_name": user.first_name,
    "last_name": user.last_name,
    "email": user.email,
    "city": "City updated",
    "description": "Description updated",
    "date_of_birth": "2000-01-11",
    "teaching_since": "2000-01-12",
    "education_set-TOTAL_FORMS": 1,
    "education_set-INITIAL_FORMS": 0,
    "education_set-MIN_NUM_FORMS": 0,
    "profilelanguagelist_set-TOTAL_FORMS": 2,
    "profilelanguagelist_set-INITIAL_FORMS": 0,
    "profilelanguagelist_set-MIN_NUM_FORMS": 1,
    "profilelanguagelist_set-0-id": "",
    "profilelanguagelist_set-0-profile": 1,
    "profilelanguagelist_set-0-language": 1,
    "profilelanguagelist_set-0-level": 1,
    "profilelanguagelist_set-1-id": "",
    "profilelanguagelist_set-1-profile": 1,
    "profilelanguagelist_set-1-language": "",
    "profilelanguagelist_set-1-level": 0,
    "service_set-TOTAL_FORMS": 2,
    "service_set-INITIAL_FORMS": 0,
    "service_set-MIN_NUM_FORMS": 1,
    "service_set-0-id": "",
    "service_set-0-tutor": 1,
    "service_set-0-subject": 1,
    "service_set-0-session_length": 60,
    "service_set-0-price_per_hour": 100,
    "service_set-1-id": "",
    "service_set-1-tutor": 1,
    "service_set-1-subject": "",
    "service_set-1-session_length": 60,
    "service_set-1-price_per_hour": "",
}


def create_school_objects() -> None:
    """Create sample instances of the School object.

    The methods populates the temporary database
    with sample, mock instances of the School
    model so that the functionality of creating
    Education objects could be tested.
    """
    school1 = School(name="School1", country="Country", city="City")
    school1.save()
    school2 = School(name="School2", country="Country", city="City")
    school2.save()


def create_language_objects() -> None:
    """Create sample instances of the Language object.

    The methods populates the temporary database
    with sample, mock instances of the Language
    model so that the functionality of creating
    ProfileLanguageList objects could be tested.
    """
    language1 = Language(name="English")
    language1.save()
    language2 = Language(name="German")
    language2.save()


def create_subject_objects() -> None:
    """Create sample instances of the Subject object.

    The methods populates the temporary database
    with sample, mock instances of the Subject
    model so that the functionality of creating
    Service objects could be tested.
    """
    subject1 = Subject(name="Math", category=2)
    subject1.save()
    subject2 = Subject(name="English", category=0)
    subject2.save()


def create_education_objects(profile: Profile) -> None:
    """Create instances of the Education model.

        The function populates the temporary database with
        sample, mock instances of the Education model
        so that the functionality of updating these
        objects via page for updating entire profile
        could be tested.

    Args:
            profile: Instance of the Profile model
                    that the newlt created Education
                    object will be linked to.
    """
    education1 = Education(
        profile=profile,
        school=School.objects.get(pk=1),
        start_date="2000-01-11",
        end_date="2003-01-11",
        degree="Bachelor",
        additional_info="Additional info about bachelor degree.",
    )
    education1.save()
    education2 = Education(
        profile=profile,
        school=School.objects.get(pk=2),
        start_date="2003-01-12",
        end_date="2005-01-12",
        degree="Master's",
        additional_info="Additional info about master degree.",
    )
    education2.save()


def create_profile_language_list_objects(profile: Profile) -> None:
    """Create instances of the ProfileLanguageList model.

        The function populates the temporary database with
        sample, mock instances of the ProfileLanguageList
        model so that the functionality of updating and
        deleting these objects via page for updating entire
        profile could be tested.

    Args:
            profile: Instance of the Profile model
                    that the newly created ProfileLanguageList
                    object will be linked to.
    """
    profile_language_list1 = ProfileLanguageList(
        language=Language.objects.get(pk=1),
        profile=profile,
        level=0,
    )
    profile_language_list1.save()

    profile_language_list2 = ProfileLanguageList(
        language=Language.objects.get(pk=2),
        profile=profile,
        level=1,
    )
    profile_language_list2.save()


def create_service_objects(profile: Profile) -> None:
    """Create instances of the Service model.

        The function populates the temporary database with
        sample, mock instances of the Service
        model so that the functionality of updating and
        deleting these objects via page for updating entire
        profile could be tested.

    Args:
            profile: Instance of the Profile model
                    that the newly created Service
                    object will be linked to.
    """
    service1 = Service(
        tutor=profile,
        subject=Subject.objects.get(pk=1),
        number_of_hours=1,
        price_per_hour=100,
        session_length=60,
        is_default=True,
    )
    service1.save()

    service2 = Service(
        tutor=profile,
        subject=Subject.objects.get(pk=2),
        number_of_hours=1,
        price_per_hour=120,
        session_length=60,
        is_default=True,
    )
    service2.save()


class TestUpdateProfileStudent(TestCaseUserUtils):
    @classmethod
    def setUpTestData(cls):
        """Populate the database with sample values of some of the models."""
        create_school_objects()
        create_language_objects()
        create_subject_objects()

    def test_correct_update_form_user_correctly_redirected(self):
        self._register_user("tutor1", student=False)
        user = User.objects.get(pk=1)
        res = self.client.post(
            reverse("profiles:tutor_update", kwargs={"pk": 1}),
            data=CORRECT_UPDATE_TUTOR_PROFILE_DATA(user),
        )
        self.assertRedirects(res, reverse("home:home"))

    def test_correct_update_form_profile_object_updated(self):
        self._register_user("tutor1", student=False)
        user = User.objects.get(pk=1)
        res = self.client.post(
            reverse("profiles:student_update", kwargs={"pk": 1}),
            data=CORRECT_UPDATE_TUTOR_PROFILE_DATA(user),
            follow=True,
        )
        self.assertEqual(res.status_code, 200)

        profile = Profile.objects.get(pk=1)

        self.assertEqual(profile.city, "City updated")
        self.assertEqual(profile.description, "Description updated")
        self.assertEqual(profile.date_of_birth, date(2000, 1, 11))
        self.assertEqual(profile.teaching_since, date(2000, 1, 12))

    def test_correct_update_form_with_profile_picture_profile_object_updated(self):
        self._register_user("tutor1", student=False)
        user = User.objects.get(pk=1)
        with open(
            Path(settings.BASE_DIR, "profiles", "test", "data", "new_profile_pic.jpg"),
            "rb",
        ) as f:
            data = CORRECT_UPDATE_TUTOR_PROFILE_DATA(user)
            data["profile_pic"] = f
            res = self.client.post(
                reverse("profiles:student_update", kwargs={"pk": 1}),
                data=data,
                follow=True,
            )
        self.assertEqual(res.status_code, 200)

        profile = Profile.objects.get(pk=1)

        self.assertRegex(
            profile.profile_pic.url,
            re.compile(
                r"/media/profiles/images/user_1/profile_pic/new_profile_pic(.*).jpg"
            ),
        )

    def test_correct_update_form_user_object_updated(self):
        self._register_user("tutor1", student=False)
        user = User.objects.get(pk=1)

        data = CORRECT_UPDATE_TUTOR_PROFILE_DATA(user)
        data["first_name"] = "First name updated"
        data["last_name"] = "Last name updated"
        data["email"] = "email_update@mail.com"

        res = self.client.post(
            reverse("profiles:student_update", kwargs={"pk": 1}),
            data=data,
            follow=True,
        )

        self.assertEqual(res.status_code, 200)

        user = User.objects.get(pk=1)

        self.assertEqual(user.first_name, "First name updated")
        self.assertEqual(user.last_name, "Last name updated")
        self.assertEqual(user.email, "email_update@mail.com")

    def test_correct_update_form_one_education_object_created(self):
        self._register_user("tutor1", student=False)
        user = User.objects.get(pk=1)

        data = CORRECT_UPDATE_TUTOR_PROFILE_DATA(user)
        data["education_set-0-school"] = 1
        data["education_set-0-degree"] = "Degree"
        data["education_set-0-start_date"] = "2000-01-11"
        data["education_set-0-end_date"] = "2003-01-11"
        data["education_set-0-additional_info"] = "Additional info"

        res = self.client.post(
            reverse("profiles:student_update", kwargs={"pk": 1}),
            data=data,
            follow=True,
        )

        self.assertEqual(res.status_code, 200)

        education = Education.objects.get(pk=1)

        self.assertEqual(education.school, School.objects.get(pk=1))
        self.assertEqual(education.degree, "Degree")
        self.assertEqual(education.start_date, date(2000, 1, 11))
        self.assertEqual(education.end_date, date(2003, 1, 11))
        self.assertEqual(education.additional_info, "Additional info")

    def test_correct_update_form_two_education_objects_created(self):
        self._register_user("tutor1", student=False)
        user = User.objects.get(pk=1)

        data = CORRECT_UPDATE_TUTOR_PROFILE_DATA(user)
        data["education_set-TOTAL_FORMS"] = 2
        data["education_set-MIN_NUM_FORMS"] = 1
        data["education_set-0-school"] = 1
        data["education_set-0-degree"] = "Degree1"
        data["education_set-0-start_date"] = "2000-01-11"
        data["education_set-0-end_date"] = "2003-01-11"
        data["education_set-0-additional_info"] = "Additional info1"
        data["education_set-1-school"] = 2
        data["education_set-1-degree"] = "Degree2"
        data["education_set-1-start_date"] = "2003-01-12"
        data["education_set-1-end_date"] = "2005-01-12"
        data["education_set-1-additional_info"] = "Additional info2"

        res = self.client.post(
            reverse("profiles:student_update", kwargs={"pk": 1}),
            data=data,
            follow=True,
        )

        self.assertEqual(res.status_code, 200)

        education1 = Education.objects.get(pk=1)

        self.assertEqual(education1.school, School.objects.get(pk=1))
        self.assertEqual(education1.degree, "Degree1")
        self.assertEqual(education1.start_date, date(2000, 1, 11))
        self.assertEqual(education1.end_date, date(2003, 1, 11))
        self.assertEqual(education1.additional_info, "Additional info1")

        education2 = Education.objects.get(pk=2)

        self.assertEqual(education2.school, School.objects.get(pk=2))
        self.assertEqual(education2.degree, "Degree2")
        self.assertEqual(education2.start_date, date(2003, 1, 12))
        self.assertEqual(education2.end_date, date(2005, 1, 12))
        self.assertEqual(education2.additional_info, "Additional info2")

    def test_correct_update_form_education_object_updated(self):
        self._register_user("tutor1", student=False)
        create_education_objects(profile=Profile.objects.get(pk=1))

        education1 = Education.objects.get(pk=1)
        education2 = Education.objects.get(pk=2)

        user = User.objects.get(pk=1)
        data = CORRECT_UPDATE_TUTOR_PROFILE_DATA(user)
        data["education_set-TOTAL_FORMS"] = 2
        data["education_set-INITIAL_FORMS"] = 1
        data["education_set-MIN_NUM_FORMS"] = 0
        data["education_set-0-id"] = 1
        data["education_set-0-profile"] = 1
        data["education_set-0-school"] = 1
        data["education_set-0-degree"] = "Bachelor updated"
        data["education_set-0-start_date"] = "2001-01-11"
        data["education_set-0-end_date"] = "2004-01-11"
        data["education_set-0-additional_info"] = "Additional info1 updated"
        data["education_set-1-id"] = 2
        data["education_set-1-profile"] = 1
        data["education_set-1-school"] = 2
        data["education_set-1-degree"] = education2.degree
        data["education_set-1-start_date"] = education2.start_date
        data["education_set-1-end_date"] = education2.end_date
        data["education_set-1-additional_info"] = education2.end_date

        self.client.post(
            reverse("profiles:student_update", kwargs={"pk": 1}),
            data=data,
            follow=True,
        )

        education1.refresh_from_db()

        self.assertEqual(education1.degree, "Bachelor updated")
        self.assertEqual(education1.start_date, date(2001, 1, 11))
        self.assertEqual(education1.end_date, date(2004, 1, 11))
        self.assertEqual(education1.additional_info, "Additional info1 updated")

    def test_correct_update_form_profile_language_list_object_created(self):
        self._register_user("tutor1", student=False)
        user = User.objects.get(pk=1)
        self.client.post(
            reverse("profiles:tutor_update", kwargs={"pk": 1}),
            data=CORRECT_UPDATE_TUTOR_PROFILE_DATA(user),
        )

        profile_language_list_object = ProfileLanguageList.objects.get(profile=1)
        self.assertEqual(
            profile_language_list_object.language, Language.objects.get(pk=1)
        )
        self.assertEqual(profile_language_list_object.level, 1)

        self.assertEqual(len(ProfileLanguageList.objects.all()), 1)

    def test_correct_update_form_service_object_created(self):
        self._register_user("tutor1", student=False)
        user = User.objects.get(pk=1)
        self.client.post(
            reverse("profiles:tutor_update", kwargs={"pk": 1}),
            data=CORRECT_UPDATE_TUTOR_PROFILE_DATA(user),
        )

        service_object = Service.objects.get(tutor=1)
        self.assertEqual(service_object.subject, Subject.objects.get(pk=1))
        self.assertEqual(service_object.session_length, 60)
        self.assertEqual(service_object.price_per_hour, 100)

        self.assertEqual(len(Service.objects.all()), 1)

    def test_service_object_already_in_db_informatio_displayed(self):
        self._register_user("tutor1", student=False)
        profile = Profile.objects.get(pk=1)
        create_service_objects(profile)

        res = self.client.get(
            reverse("profiles:tutor_update", kwargs={"pk": 1}),
        )

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
            '<input type="hidden" name="service_set-2-id" id="id_service_set-2-id">',
            html=True,
        )

    def test_correct_update_form_service_object_updated(self):
        self._register_user("tutor1", student=False)
        profile = Profile.objects.get(pk=1)
        user = User.objects.get(pk=1)
        create_service_objects(profile)

        service1 = Service.objects.get(pk=1)
        self.assertEqual(service1.session_length, 60)
        self.assertEqual(service1.price_per_hour, 100)

        data = CORRECT_UPDATE_TUTOR_PROFILE_DATA(user)
        update_data = {
            "service_set-TOTAL_FORMS": 3,
            "service_set-INITIAL_FORMS": 2,
            "service_set-MIN_NUM_FORMS": 1,
            "service_set-0-id": 1,
            "service_set-0-tutor": 1,
            "service_set-0-subject": 1,
            "service_set-0-session_length": 80,
            "service_set-0-price_per_hour": 120,
            "service_set-1-id": 2,
            "service_set-1-tutor": 1,
            "service_set-1-subject": 2,
            "service_set-1-session_length": 60,
            "service_set-1-price_per_hour": 120,
            "service_set-2-id": "",
            "service_set-2-tutor": 1,
            "service_set-2-subject": "",
            "service_set-2-session_length": 60,
            "service_set-2-price_per_hour": "",
        }
        data.update(update_data)

        self.client.post(
            reverse("profiles:tutor_update", kwargs={"pk": 1}), data=data, follow=True
        )

        service1.refresh_from_db()
        self.assertEqual(service1.session_length, 80)
        self.assertEqual(service1.price_per_hour, 120)

    def test_profile_language_object_already_in_db_information_displayed(self):
        self._register_user("tutor1", student=False)
        profile = Profile.objects.get(pk=1)
        create_profile_language_list_objects(profile)

        res = self.client.get(
            reverse("profiles:tutor_update", kwargs={"pk": 1}),
        )

        self.assertContains(
            res,
            '<input type="hidden" name="profilelanguagelist_set-0-id" value="1" id="id_profilelanguagelist_set-0-id">',
            html=True,
        )
        self.assertContains(
            res,
            '<input type="hidden" name="profilelanguagelist_set-1-id" value="2" id="id_profilelanguagelist_set-1-id">',
            html=True,
        )
        self.assertContains(
            res,
            '<input type="hidden" name="profilelanguagelist_set-2-id" id="id_profilelanguagelist_set-2-id">',
            html=True,
        )

    def test_correct_update_form_profile_language_list_object_updated(self):
        self._register_user("tutor1", student=False)
        profile = Profile.objects.get(pk=1)
        user = User.objects.get(pk=1)
        create_profile_language_list_objects(profile)

        profile_language_list1 = ProfileLanguageList.objects.get(pk=1)
        self.assertEqual(profile_language_list1.language, Language.objects.get(pk=1))
        self.assertEqual(profile_language_list1.level, 0)

        data = CORRECT_UPDATE_TUTOR_PROFILE_DATA(user)
        update_data = {
            "profilelanguagelist_set-TOTAL_FORMS": 3,
            "profilelanguagelist_set-INITIAL_FORMS": 2,
            "profilelanguagelist_set-MIN_NUM_FORMS": 1,
            "profilelanguagelist_set-0-id": 1,
            "profilelanguagelist_set-0-profile": 1,
            "profilelanguagelist_set-0-language": 2,
            "profilelanguagelist_set-0-level": 1,
            "profilelanguagelist_set-1-id": 2,
            "profilelanguagelist_set-1-profile": 1,
            "profilelanguagelist_set-1-language": 2,
            "profilelanguagelist_set-1-level": 1,
            "profilelanguagelist_set-2-id": "",
            "profilelanguagelist_set-2-profile": 1,
            "profilelanguagelist_set-2-language": "",
            "profilelanguagelist_set-2-level": 0,
        }
        data.update(update_data)

        self.client.post(
            reverse("profiles:tutor_update", kwargs={"pk": 1}), data=data, follow=True
        )

        profile_language_list1.refresh_from_db()
        self.assertEqual(profile_language_list1.language, Language.objects.get(pk=2))
        self.assertEqual(profile_language_list1.level, 1)

    def test_education_object_already_in_db_infomation_displayed(self):
        self._register_user("tutor1", student=False)
        profile = Profile.objects.get(pk=1)
        create_education_objects(profile)

        res = self.client.get(
            reverse("profiles:tutor_update", kwargs={"pk": 1}),
        )

        self.assertContains(
            res,
            '<input type="hidden" name="education_set-0-id" value="1" id="id_education_set-0-id">',
            html=True,
        )
        self.assertContains(
            res,
            '<input type="hidden" name="education_set-1-id" value="2" id="id_education_set-1-id">',
            html=True,
        )
        self.assertContains(
            res,
            '<input type="hidden" name="education_set-2-id" id="id_education_set-2-id">',
            html=True,
        )

    def test_service_object_already_in_db_form_to_delete_removed_from_db(self):
        self._register_user("tutor1", student=False)
        profile = Profile.objects.get(pk=1)
        user = User.objects.get(pk=1)
        create_service_objects(profile)

        self.client.post(
            reverse("profiles:tutor_update", kwargs={"pk": 1}),
            data={
                "first_name": user.first_name,
                "last_name": user.last_name,
                "email": user.email,
                "city": "City updated",
                "description": "Description updated",
                "date_of_birth": "2000-01-11",
                "teaching_since": "2000-01-12",
                "education_set-TOTAL_FORMS": 1,
                "education_set-INITIAL_FORMS": 0,
                "education_set-MIN_NUM_FORMS": 0,
                "profilelanguagelist_set-TOTAL_FORMS": 2,
                "profilelanguagelist_set-INITIAL_FORMS": 0,
                "profilelanguagelist_set-MIN_NUM_FORMS": 1,
                "profilelanguagelist_set-0-id": "",
                "profilelanguagelist_set-0-profile": 1,
                "profilelanguagelist_set-0-language": 1,
                "profilelanguagelist_set-0-level": 1,
                "profilelanguagelist_set-1-id": "",
                "profilelanguagelist_set-1-profile": 1,
                "profilelanguagelist_set-1-language": "",
                "profilelanguagelist_set-1-level": 0,
                "service_set-TOTAL_FORMS": 3,
                "service_set-INITIAL_FORMS": 2,
                "service_set-MIN_NUM_FORMS": 1,
                "service_set-0-id": 1,
                "service_set-0-tutor": 1,
                "service_set-0-subject": 1,
                "service_set-0-session_length": 60,
                "service_set-0-price_per_hour": 100,
                "service_set-0-DELETE": "on",
                "service_set-1-id": 2,
                "service_set-1-tutor": 1,
                "service_set-1-subject": 2,
                "service_set-1-session_length": 60,
                "service_set-1-price_per_hour": 120,
                "service_set-2-id": "",
                "service_set-2-tutor": 1,
                "service_set-2-subject": "",
                "service_set-2-session_length": 60,
                "service_set-2-price_per_hour": "",
            },
            follow=True,
        )

        self.assertEqual(len(Service.objects.all()), 1)
        self.assertEqual(Service.objects.all()[0].pk, 2)

    def test_profile_language_list_object_already_in_db_form_to_delete_removed_from_db(
        self,
    ):
        self._register_user("tutor1", student=False)
        profile = Profile.objects.get(pk=1)
        user = User.objects.get(pk=1)
        create_profile_language_list_objects(profile)

        self.client.post(
            reverse("profiles:tutor_update", kwargs={"pk": 1}),
            data={
                "first_name": user.first_name,
                "last_name": user.last_name,
                "email": user.email,
                "city": "City updated",
                "description": "Description updated",
                "date_of_birth": "2000-01-11",
                "teaching_since": "2000-01-12",
                "education_set-TOTAL_FORMS": 1,
                "education_set-INITIAL_FORMS": 0,
                "education_set-MIN_NUM_FORMS": 0,
                "profilelanguagelist_set-TOTAL_FORMS": 3,
                "profilelanguagelist_set-INITIAL_FORMS": 2,
                "profilelanguagelist_set-MIN_NUM_FORMS": 1,
                "profilelanguagelist_set-0-id": 1,
                "profilelanguagelist_set-0-profile": 1,
                "profilelanguagelist_set-0-language": 1,
                "profilelanguagelist_set-0-level": 0,
                "profilelanguagelist_set-0-DELETE": "on",
                "profilelanguagelist_set-1-id": 2,
                "profilelanguagelist_set-1-profile": 1,
                "profilelanguagelist_set-1-language": 2,
                "profilelanguagelist_set-1-level": 1,
                "profilelanguagelist_set-2-id": "",
                "profilelanguagelist_set-2-profile": 1,
                "profilelanguagelist_set-2-language": "",
                "profilelanguagelist_set-2-level": 0,
                "service_set-TOTAL_FORMS": 2,
                "service_set-INITIAL_FORMS": 0,
                "service_set-MIN_NUM_FORMS": 1,
                "service_set-0-id": "",
                "service_set-0-tutor": 1,
                "service_set-0-subject": 1,
                "service_set-0-session_length": 60,
                "service_set-0-price_per_hour": 100,
                "service_set-1-id": "",
                "service_set-1-tutor": 1,
                "service_set-1-subject": "",
                "service_set-1-session_length": 60,
                "service_set-1-price_per_hour": "",
            },
            follow=True,
        )
        self.assertEqual(len(ProfileLanguageList.objects.all()), 1)
        self.assertEqual(ProfileLanguageList.objects.all()[0].pk, 2)

    def test_education_object_already_in_db_form_to_delete_removed_from_db(self):
        self._register_user("tutor1", student=False)
        profile = Profile.objects.get(pk=1)
        user = User.objects.get(pk=1)
        create_education_objects(profile)

        self.client.post(
            reverse("profiles:tutor_update", kwargs={"pk": 1}),
            data={
                "first_name": user.first_name,
                "last_name": user.last_name,
                "email": user.email,
                "city": "City updated",
                "description": "Description updated",
                "date_of_birth": "2000-01-11",
                "teaching_since": "2000-01-12",
                "education_set-TOTAL_FORMS": 3,
                "education_set-INITIAL_FORMS": 2,
                "education_set-MIN_NUM_FORMS": 0,
                "education_set-0-profile": 1,
                "education_set-0-id": 1,
                "education_set-0-school": 1,
                "education_set-0-degree": "Bachelor",
                "education_set-0-start_date": "2000-01-11",
                "education_set-0-end_date": "2003-01-11",
                "education_set-0-additional_info": "Additional info about bachelor degree.",
                "education_set-0-DELETE": "on",
                "education_set-1-profile": 1,
                "education_set-1-id": 1,
                "education_set-1-school": 2,
                "education_set-1-degree": "Master's",
                "education_set-1-start_date": "2003-01-12",
                "education_set-1-end_date": "2005-01-12",
                "education_set-1-additional_info": "Additional info about master degree.",
                "education_set-2-profile": 1,
                "education_set-2-id": "",
                "education_set-2-school": "",
                "education_set-2-degree": "",
                "education_set-2-start_date": "",
                "education_set-2-end_date": "",
                "education_set-2-additional_info": "",
                "profilelanguagelist_set-TOTAL_FORMS": 2,
                "profilelanguagelist_set-INITIAL_FORMS": 0,
                "profilelanguagelist_set-MIN_NUM_FORMS": 1,
                "profilelanguagelist_set-0-id": "",
                "profilelanguagelist_set-0-profile": 1,
                "profilelanguagelist_set-0-language": 1,
                "profilelanguagelist_set-0-level": 1,
                "profilelanguagelist_set-1-id": "",
                "profilelanguagelist_set-1-profile": 1,
                "profilelanguagelist_set-1-language": "",
                "profilelanguagelist_set-1-level": 0,
                "service_set-TOTAL_FORMS": 2,
                "service_set-INITIAL_FORMS": 0,
                "service_set-MIN_NUM_FORMS": 1,
                "service_set-0-id": "",
                "service_set-0-tutor": 1,
                "service_set-0-subject": 1,
                "service_set-0-session_length": 60,
                "service_set-0-price_per_hour": 100,
                "service_set-1-id": "",
                "service_set-1-tutor": 1,
                "service_set-1-subject": "",
                "service_set-1-session_length": 60,
                "service_set-1-price_per_hour": "",
            },
            follow=True,
        )

        self.assertEqual(len(Education.objects.all()), 1)
        self.assertEqual(Education.objects.all()[0].pk, 2)

    @parameterized.expand(
        [
            (
                {
                    "city": "",
                },
                "This field is required.",
            ),
            (
                {
                    "description": "",
                },
                "This field is required.",
            ),
            (
                {
                    "date_of_birth": "",
                },
                "This field is required.",
            ),
            (
                {
                    "date_of_birth": "xyz",
                },
                "Enter a valid date.",
            ),
            (
                {
                    "city": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
                },
                "Ensure this value has at most 100 characters",
            ),
        ]
    )
    def test_incorrect_update_form_with_profile_object_errors_message_displayed(
        self, erroneous_data, error_message
    ):
        self._register_user("tutor1", student=False)
        data = CORRECT_UPDATE_TUTOR_PROFILE_DATA(User.objects.get(pk=1))
        data.update(erroneous_data)

        res = self.client.post(
            reverse("profiles:tutor_update", kwargs={"pk": 1}),
            data=data,
            follow=True,
        )
        self.assertContains(res, error_message)

    def test_incorrect_update_form_profile_pic_file_too_large_error_message_disaplyed(
        self,
    ):
        self._register_user("tutor1", student=False)
        user = User.objects.get(pk=1)
        data = CORRECT_UPDATE_TUTOR_PROFILE_DATA(user)
        with open(
            Path(
                settings.BASE_DIR,
                "profiles",
                "test",
                "data",
                "profile_pic_too_large.jpg",
            ),
            "rb",
        ) as f:
            data["profile_pic"] = f
            res = self.client.post(
                reverse("profiles:tutor_update", kwargs={"pk": 1}),
                data=data,
                follow=True,
            )
        self.assertContains(res, "File too large. Size should not exceed 1 MB.")

    @parameterized.expand(
        [
            (
                {
                    "education_set-TOTAL_FORMS": 1,
                    "education_set-INITIAL_FORMS": 0,
                    "education_set-MIN_NUM_FORMS": 0,
                    "education_set-0-id": "",
                    "education_set-0-profile": 1,
                    "education_set-0-school": "",
                    "education_set-0-degree": "Degree",
                    "education_set-0-start_date": "2000-01-11",
                    "education_set-0-end_date": "2003-01-11",
                    "education_set-0-additional_info": "Additional info",
                },
                "This field is required.",
            ),
            (
                {
                    "education_set-TOTAL_FORMS": 1,
                    "education_set-INITIAL_FORMS": 0,
                    "education_set-MIN_NUM_FORMS": 0,
                    "education_set-0-id": "",
                    "education_set-0-profile": 1,
                    "education_set-0-school": "1",
                    "education_set-0-degree": "",
                    "education_set-0-start_date": "2000-01-11",
                    "education_set-0-end_date": "2003-01-11",
                    "education_set-0-additional_info": "Additional info",
                },
                "This field is required.",
            ),
            (
                {
                    "education_set-TOTAL_FORMS": 1,
                    "education_set-INITIAL_FORMS": 0,
                    "education_set-MIN_NUM_FORMS": 0,
                    "education_set-0-id": "",
                    "education_set-0-profile": 1,
                    "education_set-0-school": 1,
                    "education_set-0-degree": "Degree",
                    "education_set-0-start_date": "",
                    "education_set-0-end_date": "2003-01-11",
                    "education_set-0-additional_info": "Additional info",
                },
                "This field is required.",
            ),
            (
                {
                    "education_set-TOTAL_FORMS": 1,
                    "education_set-INITIAL_FORMS": 0,
                    "education_set-MIN_NUM_FORMS": 0,
                    "education_set-0-id": "",
                    "education_set-0-profile": 1,
                    "education_set-0-school": 1,
                    "education_set-0-degree": "Degree",
                    "education_set-0-start_date": "2000-01-11",
                    "education_set-0-end_date": "",
                    "education_set-0-additional_info": "Additional info",
                },
                "This field is required.",
            ),
            (
                {
                    "education_set-TOTAL_FORMS": 1,
                    "education_set-INITIAL_FORMS": 0,
                    "education_set-MIN_NUM_FORMS": 0,
                    "education_set-0-id": "",
                    "education_set-0-profile": 1,
                    "education_set-0-school": 1,
                    "education_set-0-degree": "Degree",
                    "education_set-0-start_date": "2000-01-11",
                    "education_set-0-end_date": "2003-01-11",
                    "education_set-0-additional_info": "",
                },
                "This field is required.",
            ),
            (
                {
                    "education_set-TOTAL_FORMS": 1,
                    "education_set-INITIAL_FORMS": 0,
                    "education_set-MIN_NUM_FORMS": 0,
                    "education_set-0-id": "",
                    "education_set-0-profile": 1,
                    "education_set-0-school": "Non-existent school ID",
                    "education_set-0-degree": "Degree",
                    "education_set-0-start_date": "2000-01-11",
                    "education_set-0-end_date": "2003-01-11",
                    "education_set-0-additional_info": "Additional info",
                },
                "Select a valid choice. That choice is not one of the available choices.",
            ),
            (
                {
                    "education_set-TOTAL_FORMS": 1,
                    "education_set-INITIAL_FORMS": 0,
                    "education_set-MIN_NUM_FORMS": 0,
                    "education_set-0-id": "",
                    "education_set-0-profile": 1,
                    "education_set-0-school": 1,
                    "education_set-0-degree": "Degree",
                    "education_set-0-start_date": "2003-01-11",
                    "education_set-0-end_date": "2000-01-11",
                    "education_set-0-additional_info": "Additional info",
                },
                "Start date: 2003-01-11 falls after End date: 2000-01-11",
            ),
        ]
    )
    def test_incorrect_update_form_with_education_formset_errors_no_education_objects_in_db_message_displayed(
        self, erroneous_data, error_message
    ):
        self._register_user("tutor1", student=False)
        data = CORRECT_UPDATE_TUTOR_PROFILE_DATA(User.objects.get(pk=1))
        data.update(erroneous_data)

        res = self.client.post(
            reverse("profiles:tutor_update", kwargs={"pk": 1}),
            data=data,
            follow=True,
        )
        self.assertQuerySetEqual(Education.objects.all(), [])
        self.assertContains(res, error_message)

    @parameterized.expand(
        [
            (
                {
                    "service_set-0-subject": "",
                },
                "This field is required.",
            ),
            (
                {
                    "service_set-0-session_length": "",
                },
                "This field is required.",
            ),
            (
                {
                    "service_set-0-price_per_hour": "",
                },
                "This field is required.",
            ),
        ]
    )
    def test_incorreact_update_form_with_service_formset_errors_no_service_objects_in_db_message_displayed(
        self, erroneous_data, error_message
    ):
        self._register_user("tutor1", student=False)
        data = CORRECT_UPDATE_TUTOR_PROFILE_DATA(User.objects.get(pk=1))
        data.update(erroneous_data)

        res = self.client.post(
            reverse("profiles:tutor_update", kwargs={"pk": 1}),
            data=data,
            follow=True,
        )
        self.assertQuerySetEqual(Service.objects.all(), [])
        self.assertContains(res, error_message)

    @parameterized.expand(
        [
            (
                {
                    "profilelanguagelist_set-0-language": "",
                },
                "This field is required.",
            ),
            (
                {
                    "profilelanguagelist_set-0-level": "",
                },
                "This field is required.",
            ),
        ]
    )
    def test_incorreact_update_form_with_profile_language_list_formset_errors_no_objects_in_db_message_displayed(
        self, erroneous_data, error_message
    ):
        self._register_user("tutor1", student=False)
        data = CORRECT_UPDATE_TUTOR_PROFILE_DATA(User.objects.get(pk=1))
        data.update(erroneous_data)

        res = self.client.post(
            reverse("profiles:tutor_update", kwargs={"pk": 1}),
            data=data,
            follow=True,
        )
        self.assertQuerySetEqual(ProfileLanguageList.objects.all(), [])
        self.assertContains(res, error_message)

    def test_attempting_to_edit_someone_elses_profile_redirected_warning_displayed(
        self,
    ):
        self._register_user("tutor1", student=False)
        self._register_user("tutor2", student=False)
        self.client.login(username="tutor2", password="haslo123")
        res = self.client.get(reverse("profiles:tutor_update", kwargs={"pk": 1}))

        self.assertEqual(res.status_code, 403)
        self.assertContains(
            res,
            "You are not allowe to edit other user's profile!",
            status_code=403,
            html=True,
        )

    def test_students_profile_attempting_to_access_update_tutors_profile_page_correctly_redirected(
        self,
    ):
        self._register_user("student1")
        res = self.client.get(
            reverse("profiles:tutor_update", kwargs={"pk": 1}), follow=True
        )

        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.redirect_chain, [("/profiles/student/update/1", 302)])
