"""Test for the functionality of updating Student's profile."""

import re
from datetime import date
from pathlib import Path

from django.conf import settings
from django.contrib.auth.models import User
from django.urls import reverse
from parameterized import parameterized

from profiles.models import Education, Profile, School
from utils.testing import TestCaseUserUtils


class TestUpdateProfileStudent(TestCaseUserUtils):
    def _create_school_objects(self) -> None:
        """Create sample instances of the Scool object.

        The methods populates the temporary database
        with sample, mock instances of the School
        model so that the functionality of creating
        Education objects could be tested.
        """
        school1 = School(name="School1", country="Country", city="City")
        school1.save()
        school2 = School(name="School2", country="Country", city="City")
        school2.save()

    def _create_education_objects(self, profile: Profile) -> None:
        """Create instances of the Education model.

        The method populated the temporary database with
        sample, mock instances of the Education model
        so that the functionality of updating these
        objects via page for updating entire profile
        could be tested.

        Args:
            profile: Instance of the Profile model
                    that the newlt created Education
                    object will be linked to.
        """
        self._create_school_objects()
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

    def test_correct_update_form_user_correctly_redirected(self):
        self._register_user("student1")
        user = User.objects.get(pk=1)
        res = self.client.post(
            reverse("profiles:update", kwargs={"pk": 1}),
            {
                "first_name": user.first_name,
                "last_name": user.last_name,
                "email": user.email,
                "city": "City updated",
                "description": "Description updated",
                "date_of_birth": "2000-01-11",
                "education_set-TOTAL_FORMS": 1,
                "education_set-INITIAL_FORMS": 0,
                "education_set-MIN_NUM_FORMS": 0,
            },
        )
        self.assertRedirects(res, reverse("home:home"))

    def test_correct_update_form_profile_object_updated(self):
        self._register_user("student1")
        user = User.objects.get(pk=1)
        res = self.client.post(
            reverse("profiles:update", kwargs={"pk": 1}),
            {
                "first_name": user.first_name,
                "last_name": user.last_name,
                "email": user.email,
                "city": "City updated",
                "description": "Description updated",
                "date_of_birth": "2000-01-11",
                "education_set-TOTAL_FORMS": 1,
                "education_set-INITIAL_FORMS": 0,
                "education_set-MIN_NUM_FORMS": 0,
            },
            follow=True,
        )
        self.assertEqual(res.status_code, 200)

        profile = Profile.objects.get(pk=1)

        self.assertEqual(profile.city, "City updated")
        self.assertEqual(profile.description, "Description updated")
        self.assertEqual(profile.date_of_birth, date(2000, 1, 11))

    def test_correct_update_form_with_profile_picture_profile_object_updated(self):
        self._register_user("student1")
        user = User.objects.get(pk=1)
        with open(
            Path(settings.BASE_DIR, "profiles", "test", "data", "new_profile_pic.jpg"),
            "rb",
        ) as f:
            res = self.client.post(
                reverse("profiles:update", kwargs={"pk": 1}),
                {
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "email": user.email,
                    "profile_pic": f,
                    "city": "City updated",
                    "description": "Description updated",
                    "date_of_birth": "2000-01-11",
                    "education_set-TOTAL_FORMS": 1,
                    "education_set-INITIAL_FORMS": 0,
                    "education_set-MIN_NUM_FORMS": 0,
                },
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
        self._register_user("student1")
        res = self.client.post(
            reverse("profiles:update", kwargs={"pk": 1}),
            {
                "first_name": "First name updated",
                "last_name": "Last name updated",
                "email": "new_email@mail.com",
                "city": "City updated",
                "description": "Description updated",
                "date_of_birth": "2000-01-11",
                "education_set-TOTAL_FORMS": 1,
                "education_set-INITIAL_FORMS": 0,
                "education_set-MIN_NUM_FORMS": 0,
            },
            follow=True,
        )
        self.assertEqual(res.status_code, 200)

        user = User.objects.get(pk=1)

        self.assertEqual(user.first_name, "First name updated")
        self.assertEqual(user.last_name, "Last name updated")
        self.assertEqual(user.email, "new_email@mail.com")

    def test_correct_update_form_one_education_object_created(self):
        self._register_user("student1")
        self._create_school_objects()
        res = self.client.post(
            reverse("profiles:update", kwargs={"pk": 1}),
            {
                "first_name": "First name updated",
                "last_name": "Last name updated",
                "email": "new_email@mail.com",
                "city": "City updated",
                "description": "Description updated",
                "date_of_birth": "2000-01-11",
                "education_set-TOTAL_FORMS": 1,
                "education_set-INITIAL_FORMS": 0,
                "education_set-MIN_NUM_FORMS": 0,
                "education_set-0-school": 1,
                "education_set-0-degree": "Degree",
                "education_set-0-start_date": "2000-01-11",
                "education_set-0-end_date": "2003-01-11",
                "education_set-0-additional_info": "Additional info",
            },
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
        self._register_user("student1")
        self._create_school_objects()
        res = self.client.post(
            reverse("profiles:update", kwargs={"pk": 1}),
            {
                "first_name": "First name updated",
                "last_name": "Last name updated",
                "email": "new_email@mail.com",
                "city": "City updated",
                "description": "Description updated",
                "date_of_birth": "2000-01-11",
                "education_set-TOTAL_FORMS": 2,
                "education_set-INITIAL_FORMS": 0,
                "education_set-MIN_NUM_FORMS": 1,
                "education_set-0-school": 1,
                "education_set-0-degree": "Degree1",
                "education_set-0-start_date": "2000-01-11",
                "education_set-0-end_date": "2003-01-11",
                "education_set-0-additional_info": "Additional info1",
                "education_set-1-school": 2,
                "education_set-1-degree": "Degree2",
                "education_set-1-start_date": "2003-01-12",
                "education_set-1-end_date": "2005-01-12",
                "education_set-1-additional_info": "Additional info2",
            },
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
        self._register_user("student1")
        self._create_education_objects(profile=Profile.objects.get(pk=1))

        education1 = Education.objects.get(pk=1)

        education2 = Education.objects.get(pk=2)
        res = self.client.post(
            reverse("profiles:update", kwargs={"pk": 1}),
            {
                "first_name": "First name updated",
                "last_name": "Last name updated",
                "email": "new_email@mail.com",
                "city": "City updated",
                "description": "Description updated",
                "date_of_birth": "2000-01-11",
                "education_set-TOTAL_FORMS": 2,
                "education_set-INITIAL_FORMS": 1,
                "education_set-MIN_NUM_FORMS": 0,
                "education_set-0-id": 1,
                "education_set-0-profile": 1,
                "education_set-0-school": 1,
                "education_set-0-degree": "Bachelor updated",
                "education_set-0-start_date": "2001-01-11",
                "education_set-0-end_date": "2004-01-11",
                "education_set-0-additional_info": "Additional info1 updated",
                "education_set-1-id": 2,
                "education_set-1-profile": 1,
                "education_set-1-school": 2,
                "education_set-1-degree": education2.degree,
                "education_set-1-start_date": education2.start_date,
                "education_set-1-end_date": education2.end_date,
                "education_set-1-additional_info": education2.end_date,
            },
            follow=True,
        )

        education1.refresh_from_db()

        self.assertEqual(education1.degree, "Bachelor updated")
        self.assertEqual(education1.start_date, date(2001, 1, 11))
        self.assertEqual(education1.end_date, date(2004, 1, 11))
        self.assertEqual(education1.additional_info, "Additional info1 updated")

    @parameterized.expand(
        [
            (
                lambda user: {
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "email": user.email,
                    "city": "",
                    "description": "Description updated",
                    "date_of_birth": "2000-01-11",
                    "education_set-TOTAL_FORMS": 1,
                    "education_set-INITIAL_FORMS": 0,
                    "education_set-MIN_NUM_FORMS": 0,
                },
                "This field is required.",
            ),
            (
                lambda user: {
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "email": user.email,
                    "city": "City",
                    "description": "",
                    "date_of_birth": "2000-01-11",
                    "education_set-TOTAL_FORMS": 1,
                    "education_set-INITIAL_FORMS": 0,
                    "education_set-MIN_NUM_FORMS": 0,
                },
                "This field is required.",
            ),
            (
                lambda user: {
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "email": user.email,
                    "city": "City",
                    "description": "Description updated",
                    "date_of_birth": "",
                    "education_set-TOTAL_FORMS": 1,
                    "education_set-INITIAL_FORMS": 0,
                    "education_set-MIN_NUM_FORMS": 0,
                },
                "This field is required.",
            ),
            (
                lambda user: {
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "email": user.email,
                    "city": "City",
                    "description": "Description updated",
                    "date_of_birth": "xyz",
                    "education_set-TOTAL_FORMS": 1,
                    "education_set-INITIAL_FORMS": 0,
                    "education_set-MIN_NUM_FORMS": 0,
                },
                "Enter a valid date.",
            ),
            (
                lambda user: {
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "email": user.email,
                    "city": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
                    "description": "Description updated",
                    "date_of_birth": "2000-01-11",
                    "education_set-TOTAL_FORMS": 1,
                    "education_set-INITIAL_FORMS": 0,
                    "education_set-MIN_NUM_FORMS": 0,
                },
                "Ensure this value has at most 100 characters",
            ),
        ]
    )
    def test_incorrect_update_form_with_profile_object_errors_message_displayed(
        self, data, error_message
    ):
        self._register_user("student1")
        user = User.objects.get(pk=1)
        res = self.client.post(
            reverse("profiles:update", kwargs={"pk": 1}), data=data(user), follow=True
        )
        self.assertContains(res, error_message)

    def test_incorrect_update_form_profile_pic_file_too_large_error_message_disaplyed(
        self,
    ):
        self._register_user("student1")
        user = User.objects.get(pk=1)
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
            res = self.client.post(
                reverse("profiles:update", kwargs={"pk": 1}),
                data={
                    "profile_pic": f,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "email": user.email,
                    "city": "City",
                    "description": "Description",
                    "date_of_birth": "2000-01-11",
                    "education_set-TOTAL_FORMS": 1,
                    "education_set-INITIAL_FORMS": 0,
                    "education_set-MIN_NUM_FORMS": 0,
                },
                follow=True,
            )
        self.assertContains(res, "File too large. Size should not exceed 1 MB.")

    @parameterized.expand(
        [
            (
                lambda user: {
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "email": user.email,
                    "city": "City updated",
                    "description": "Description updated",
                    "education_set-TOTAL_FORMS": 1,
                    "education_set-INITIAL_FORMS": 0,
                    "education_set-MIN_NUM_FORMS": 0,
                    "education_set-0-school": "",
                    "education_set-0-degree": "Degree",
                    "education_set-0-start_date": "2000-01-11",
                    "education_set-0-end_date": "2003-01-11",
                    "education_set-0-additional_info": "Additional info",
                },
                "This field is required.",
            ),
            (
                lambda user: {
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "email": user.email,
                    "city": "City updated",
                    "description": "Description updated",
                    "education_set-TOTAL_FORMS": 1,
                    "education_set-INITIAL_FORMS": 0,
                    "education_set-MIN_NUM_FORMS": 0,
                    "education_set-0-school": "1",
                    "education_set-0-degree": "",
                    "education_set-0-start_date": "2000-01-11",
                    "education_set-0-end_date": "2003-01-11",
                    "education_set-0-additional_info": "Additional info",
                },
                "This field is required.",
            ),
            (
                lambda user: {
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "email": user.email,
                    "city": "City updated",
                    "description": "Description updated",
                    "education_set-TOTAL_FORMS": 1,
                    "education_set-INITIAL_FORMS": 0,
                    "education_set-MIN_NUM_FORMS": 0,
                    "education_set-0-school": 1,
                    "education_set-0-degree": "Degree",
                    "education_set-0-start_date": "",
                    "education_set-0-end_date": "2003-01-11",
                    "education_set-0-additional_info": "Additional info",
                },
                "This field is required.",
            ),
            (
                lambda user: {
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "email": user.email,
                    "city": "City updated",
                    "description": "Description updated",
                    "education_set-TOTAL_FORMS": 1,
                    "education_set-INITIAL_FORMS": 0,
                    "education_set-MIN_NUM_FORMS": 0,
                    "education_set-0-school": 1,
                    "education_set-0-degree": "Degree",
                    "education_set-0-start_date": "2000-01-11",
                    "education_set-0-end_date": "",
                    "education_set-0-additional_info": "Additional info",
                },
                "This field is required.",
            ),
            (
                lambda user: {
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "email": user.email,
                    "city": "City updated",
                    "description": "Description updated",
                    "education_set-TOTAL_FORMS": 1,
                    "education_set-INITIAL_FORMS": 0,
                    "education_set-MIN_NUM_FORMS": 0,
                    "education_set-0-school": 1,
                    "education_set-0-degree": "Degree",
                    "education_set-0-start_date": "2000-01-11",
                    "education_set-0-end_date": "2003-01-11",
                    "education_set-0-additional_info": "",
                },
                "This field is required.",
            ),
            (
                lambda user: {
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "email": user.email,
                    "city": "City updated",
                    "description": "Description updated",
                    "education_set-TOTAL_FORMS": 1,
                    "education_set-INITIAL_FORMS": 0,
                    "education_set-MIN_NUM_FORMS": 0,
                    "education_set-0-school": "Non-existent school ID",
                    "education_set-0-degree": "Degree",
                    "education_set-0-start_date": "2000-01-11",
                    "education_set-0-end_date": "2003-01-11",
                    "education_set-0-additional_info": "Additional info",
                },
                "This field is required.",
            ),
            (
                lambda user: {
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "email": user.email,
                    "city": "City updated",
                    "description": "Description updated",
                    "date_of_birth": "2000-01-11",
                    "education_set-TOTAL_FORMS": 1,
                    "education_set-INITIAL_FORMS": 0,
                    "education_set-MIN_NUM_FORMS": 0,
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
        self, data, error_message
    ):
        self._register_user("student1")
        self._create_school_objects()
        user = User.objects.get(pk=1)
        res = self.client.post(
            reverse("profiles:update", kwargs={"pk": 1}), data=data(user), follow=True
        )

        self.assertQuerySetEqual(Education.objects.all(), [])
        self.assertContains(res, error_message)

    def test_attempting_to_edit_someone_elses_profile_redirected_warning_displayed(
        self,
    ):
        self._register_user("student1")
        self._register_user("student2")
        self.client.login(username="student2", password="haslo123")
        res = self.client.get(reverse("profiles:update", kwargs={"pk": 1}))

        self.assertEqual(res.status_code, 403)
        self.assertContains(
            res,
            "You are not allowe to edit other user's profile!",
            status_code=403,
            html=True
        )
