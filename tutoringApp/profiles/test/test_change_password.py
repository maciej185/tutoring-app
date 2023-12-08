"""Tests for the funcionality of changing password."""
from django.urls import reverse
from parameterized import parameterized

from utils.testing import TestCaseProfileUtils


class TestChangePassword(TestCaseProfileUtils):
    """Tests for the functionality of changing passwords."""

    @parameterized.expand([True, False])
    def test_password_changed_user_correctly_redirected(self, is_student):
        self.create_profile("user1", student=is_student)

        res = self.client.post(
            reverse("profiles:password_change"),
            {
                "old_password": "haslo123",
                "new_password1": "haslo1234",
                "new_password2": "haslo1234",
            },
            follow=True,
        )

        self.assertEqual(res.status_code, 200)
        self.assertRedirects(
            res,
            reverse("profiles:student_display", kwargs={"pk": 1})
            if is_student
            else reverse("profiles:tutor_display", kwargs={"pk": 1}),
        )

    @parameterized.expand([True, False])
    def test_password_not_changed_old_password_incorrect_message_displayed(
        self, is_student
    ):
        self.create_profile("user1", student=is_student)

        res = self.client.post(
            reverse("profiles:password_change"),
            {
                "old_password": "xxx",
                "new_password1": "haslo1234",
                "new_password2": "haslo1234",
            },
            follow=True,
        )

        self.assertEqual(res.status_code, 200)
        self.assertContains(
            res, "Your old password was entered incorrectly. Please enter it again."
        )

    @parameterized.expand([True, False])
    def test_password_not_changed_new_passwords_did_not_match_message_displayed(
        self, is_student
    ):
        self.create_profile("user1", student=is_student)

        res = self.client.post(
            reverse("profiles:password_change"),
            {
                "old_password": "haslo123",
                "new_password1": "haslo1234",
                "new_password2": "haslo12345",
            },
            follow=True,
        )

        self.assertEqual(res.status_code, 200)
        self.assertContains(res, "The two password fields didn’t match.")

    @parameterized.expand([True, False])
    def test_password_not_changed_new_password_enitirely_numeric_message_displayed(
        self, is_student
    ):
        self.create_profile("user1", student=is_student)

        res = self.client.post(
            reverse("profiles:password_change"),
            {
                "old_password": "haslo123",
                "new_password1": "12345",
                "new_password2": "12345",
            },
            follow=True,
        )

        self.assertEqual(res.status_code, 200)
        self.assertContains(res, "This password is entirely numeric.")

    @parameterized.expand([True, False])
    def test_password_not_changed_new_password_too_short_message_displayed(
        self, is_student
    ):
        self.create_profile("user1", student=is_student)

        res = self.client.post(
            reverse("profiles:password_change"),
            {
                "old_password": "haslo123",
                "new_password1": "12345",
                "new_password2": "12345",
            },
            follow=True,
        )

        self.assertEqual(res.status_code, 200)
        self.assertContains(
            res, "This password is too short. It must contain at least 8 characters."
        )
