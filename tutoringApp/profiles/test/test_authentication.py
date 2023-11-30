"""Tests for the authentication funcionalities."""
from django.contrib.auth import get_user
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from parameterized import parameterized

from profiles.forms import AccountType
from profiles.models import Profile

INCORRECT_REGISTRATION_DATA = {
    "login_taken": {
        "expected_number_of_users": 1,
        "request_infos": [
            {
                "follow": True,
                "data": {
                    "username": "username",
                    "first_name": "First name",
                    "last_name": "Last name",
                    "email": "email@mail.com",
                    "password1": "e573MrIR8XfOXma",
                    "password2": "e573MrIR8XfOXma",
                    "account_type": AccountType.STUDENT.value,
                },
            },
            {
                "follow": False,
                "data": {
                    "username": "username",
                    "first_name": "First name1",
                    "last_name": "Last name1",
                    "email": "email1@mail.com",
                    "password1": "e573MrIR8XfOXma",
                    "password2": "e573MrIR8XfOXma",
                    "account_type": AccountType.STUDENT.value,
                },
            },
            {
                "follow": True,
                "data": {
                    "username": "username",
                    "first_name": "First name",
                    "last_name": "Last name",
                    "email": "email@mail.com",
                    "password1": "e573MrIR8XfOXma",
                    "password2": "e573MrIR8XfOXma",
                    "account_type": AccountType.TUTOR.value,
                },
            },
            {
                "follow": False,
                "data": {
                    "username": "username",
                    "first_name": "First name1",
                    "last_name": "Last name1",
                    "email": "email1@mail.com",
                    "password1": "e573MrIR8XfOXma",
                    "password2": "e573MrIR8XfOXma",
                    "account_type": AccountType.TUTOR.value,
                },
            },
        ],
    },
    "email_taken": {
        "expected_number_of_users": 1,
        "request_infos": [
            {
                "follow": True,
                "data": {
                    "username": "username",
                    "first_name": "First name",
                    "last_name": "Last name",
                    "email": "email@mail.com",
                    "password1": "e573MrIR8XfOXma",
                    "password2": "e573MrIR8XfOXma",
                    "account_type": AccountType.STUDENT.value,
                },
            },
            {
                "follow": False,
                "data": {
                    "username": "username1",
                    "first_name": "First name1",
                    "last_name": "Last name1",
                    "email": "email@mail.com",
                    "password1": "e573MrIR8XfOXma",
                    "password2": "e573MrIR8XfOXma",
                    "account_type": AccountType.STUDENT.value,
                },
            },
            {
                "follow": True,
                "data": {
                    "username": "username",
                    "first_name": "First name",
                    "last_name": "Last name",
                    "email": "email@mail.com",
                    "password1": "e573MrIR8XfOXma",
                    "password2": "e573MrIR8XfOXma",
                    "account_type": AccountType.TUTOR.value,
                },
            },
            {
                "follow": False,
                "data": {
                    "username": "username1",
                    "first_name": "First name1",
                    "last_name": "Last name1",
                    "email": "email@mail.com",
                    "password1": "e573MrIR8XfOXma",
                    "password2": "e573MrIR8XfOXma",
                    "account_type": AccountType.TUTOR.value,
                },
            },
        ],
    },
    "no_first_name": {
        "expected_number_of_users": 0,
        "request_infos": [
            {
                "follow": False,
                "data": {
                    "username": "username",
                    "first_name": "",
                    "last_name": "Last name",
                    "email": "email@mail.com",
                    "password1": "e573MrIR8XfOXma",
                    "password2": "e573MrIR8XfOXma",
                    "account_type": AccountType.STUDENT.value,
                },
            },
            {
                "follow": False,
                "data": {
                    "username": "username",
                    "first_name": "",
                    "last_name": "Last name",
                    "email": "email@mail.com",
                    "password1": "e573MrIR8XfOXma",
                    "password2": "e573MrIR8XfOXma",
                    "account_type": AccountType.TUTOR.value,
                },
            },
        ],
    },
    "no_last_name": {
        "expected_number_of_users": 0,
        "request_infos": [
            {
                "follow": False,
                "data": {
                    "username": "username",
                    "first_name": "First name",
                    "last_name": "",
                    "email": "email@mail.com",
                    "password1": "e573MrIR8XfOXma",
                    "password2": "e573MrIR8XfOXma",
                    "account_type": AccountType.STUDENT.value,
                },
            },
            {
                "follow": False,
                "data": {
                    "username": "username",
                    "first_name": "First name",
                    "last_name": "",
                    "email": "email@mail.com",
                    "password1": "e573MrIR8XfOXma",
                    "password2": "e573MrIR8XfOXma",
                    "account_type": AccountType.TUTOR.value,
                },
            },
        ],
    },
    "password_too_common": {
        "expected_number_of_users": 0,
        "request_infos": [
            {
                "follow": False,
                "data": {
                    "username": "username",
                    "first_name": "First name",
                    "last_name": "Last name",
                    "email": "email@mail.com",
                    "password1": "password123",
                    "password2": "password123",
                    "account_type": AccountType.STUDENT.value,
                },
            },
            {
                "follow": False,
                "data": {
                    "username": "username",
                    "first_name": "First name",
                    "last_name": "Last name",
                    "email": "email@mail.com",
                    "password1": "password123",
                    "password2": "password123",
                    "account_type": AccountType.TUTOR.value,
                },
            },
        ],
    },
    "passwords_dont_match": {
        "expected_number_of_users": 0,
        "request_infos": [
            {
                "follow": False,
                "data": {
                    "username": "username",
                    "first_name": "First name",
                    "last_name": "Last name",
                    "email": "email@mail.com",
                    "password1": "e573MrIR8XfOXma",
                    "password2": "e573MrIR8",
                    "account_type": AccountType.STUDENT.value,
                },
            },
            {
                "follow": False,
                "data": {
                    "username": "username",
                    "first_name": "First name",
                    "last_name": "Last name",
                    "email": "email@mail.com",
                    "password1": "e573MrIR8XfOXma",
                    "password2": "e573MrIR8",
                    "account_type": AccountType.TUTOR.value,
                },
            },
        ],
    },
}


class TestAuthentication(TestCase):
    @parameterized.expand([AccountType.STUDENT.value, AccountType.TUTOR.value])
    def test_correct_registration_form_user_created(self, account_type):
        res = self.client.post(
            reverse("profiles:register"),
            {
                "username": "username",
                "first_name": "First name",
                "last_name": "Last name",
                "email": "email@mail.com",
                "password1": "e573MrIR8XfOXma",
                "password2": "e573MrIR8XfOXma",
                "account_type": account_type,
            },
        )
        self.assertEqual(res.status_code, 302)
        User.objects.get(pk=1)

    @parameterized.expand(
        [
            (
                AccountType.STUDENT.value,
                [("/profiles/create/1", 302), ("/profiles/student/update/1", 302)],
            ),
            (
                AccountType.TUTOR.value,
                [("/profiles/create/1", 302), ("/profiles/tutor/update/1", 302)],
            ),
        ]
    )
    def test_correct_registration_form_correctly_redirected(
        self, account_type, redirect_chain
    ):
        res = self.client.post(
            reverse("profiles:register"),
            {
                "username": "username",
                "first_name": "First name",
                "last_name": "Last name",
                "email": "email@mail.com",
                "password1": "e573MrIR8XfOXma",
                "password2": "e573MrIR8XfOXma",
                "account_type": account_type,
            },
            follow=True,
        )
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.redirect_chain, redirect_chain)

    @parameterized.expand([AccountType.STUDENT.value, AccountType.TUTOR.value])
    def test_correct_registration_form_user_logged_in(self, account_type):
        self.client.post(
            reverse("profiles:register"),
            {
                "username": "username",
                "first_name": "First name",
                "last_name": "Last name",
                "email": "email@mail.com",
                "password1": "e573MrIR8XfOXma",
                "password2": "e573MrIR8XfOXma",
                "account_type": account_type,
            },
            follow=True,
        )
        logged_user = get_user(self.client)
        created_user = User.objects.get(pk=1)
        self.assertEqual(logged_user, created_user)

    @parameterized.expand([AccountType.STUDENT.value, AccountType.TUTOR.value])
    def test_correct_registration_form_profile_created(self, account_type):
        self.client.post(
            reverse("profiles:register"),
            {
                "username": "username",
                "first_name": "First name",
                "last_name": "Last name",
                "email": "email@mail.com",
                "password1": "e573MrIR8XfOXma",
                "password2": "e573MrIR8XfOXma",
                "account_type": account_type,
            },
            follow=True,
        )
        Profile.objects.get(pk=1)

    def test_incorrect_registration_form_login_taken_message_displayed(self):
        responses = [
            self.client.post(
                reverse("profiles:register"),
                data=request_info["data"],
                follow=request_info["follow"],
            )
            for request_info in INCORRECT_REGISTRATION_DATA["login_taken"][
                "request_infos"
            ]
        ]

        self.assertEqual(responses[-1].status_code, 200)
        self.assertContains(responses[-1], "Username already taken.")

    def test_incorrect_registration_form_email_taken_message_displayed(self):
        responses = [
            self.client.post(
                reverse("profiles:register"),
                data=request_info["data"],
                follow=request_info["follow"],
            )
            for request_info in INCORRECT_REGISTRATION_DATA["email_taken"][
                "request_infos"
            ]
        ]

        self.assertEqual(responses[-1].status_code, 200)
        self.assertContains(responses[-1], "Email already taken.")

    def test_incorrect_registration_form_no_first_name_message_displayed(self):
        responses = [
            self.client.post(
                reverse("profiles:register"),
                data=request_info["data"],
                follow=request_info["follow"],
            )
            for request_info in INCORRECT_REGISTRATION_DATA["no_first_name"][
                "request_infos"
            ]
        ]

        self.assertEqual(responses[-1].status_code, 200)
        self.assertContains(responses[-1], "This field is required.")

    def test_incorrect_registration_form_no_last_name_message_displayed(self):
        responses = [
            self.client.post(
                reverse("profiles:register"),
                data=request_info["data"],
                follow=request_info["follow"],
            )
            for request_info in INCORRECT_REGISTRATION_DATA["no_last_name"][
                "request_infos"
            ]
        ]

        self.assertEqual(responses[-1].status_code, 200)
        self.assertContains(responses[-1], "This field is required.")

    def test_incorrect_registration_form_password_too_common_message_displayed(self):
        responses = [
            self.client.post(
                reverse("profiles:register"),
                data=request_info["data"],
                follow=request_info["follow"],
            )
            for request_info in INCORRECT_REGISTRATION_DATA["password_too_common"][
                "request_infos"
            ]
        ]

        self.assertEqual(responses[-1].status_code, 200)
        self.assertContains(responses[-1], "This password is too common.")

    def test_incorrect_registration_form_passwords_dont_match_message_displayed(self):
        responses = [
            self.client.post(
                reverse("profiles:register"),
                data=request_info["data"],
                follow=request_info["follow"],
            )
            for request_info in INCORRECT_REGISTRATION_DATA["passwords_dont_match"][
                "request_infos"
            ]
        ]

        self.assertEqual(responses[-1].status_code, 200)
        self.assertContains(responses[-1], "The two password fields didn’t match.")

    @parameterized.expand(
        [list(test_data.values()) for test_data in INCORRECT_REGISTRATION_DATA.values()]
    )
    def test_incorrect_registration_form_user_object_not_created(
        self, expected_number_of_users, request_infos
    ):
        responses = [
            self.client.post(
                reverse("profiles:register"),
                data=request_info["data"],
                follow=request_info["follow"],
            )
            for request_info in request_infos
        ]

        self.assertEqual(len(User.objects.all()), expected_number_of_users)

    @parameterized.expand(
        [list(test_data.values()) for test_data in INCORRECT_REGISTRATION_DATA.values()]
    )
    def test_incorrect_registration_form_profile_not_created(
        self, expected_number_of_users, request_infos
    ):
        responses = [
            self.client.post(
                reverse("profiles:register"),
                data=request_info["data"],
                follow=request_info["follow"],
            )
            for request_info in request_infos
        ]
        self.assertEqual(len(Profile.objects.all()), expected_number_of_users)
