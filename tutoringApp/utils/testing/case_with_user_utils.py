"""Extenstion of default TestCase with registration of new users."""
from django.test import TestCase
from django.urls import reverse

from profiles.forms import AccountType


class TestCaseUserUtils(TestCase):
    """Extension of TestCase class to add registration methods.

    The extension allows fir registering users and thus also
    creating instances of the Profile object.
    """

    def _register_user(
        self, username: str, password: str = "haslo123", student: bool = True
    ) -> None:
        """Registers a user with provided credentials.

        The method registers the user by making a request to correct
        URL that then invokes the registration view.

        Args:
            username (str): Desired username.
            password (str): Desired password.
            student (bool): Flag indicating whether the account
                            is Student or Tutor's account.
        """

        self.client.post(
            reverse("profiles:register"),
            {
                "username": username,
                "first_name": f"{username}'s first name",
                "last_name": f"{username}'s last name",
                "email": username + "@mail.com",
                "password1": password,
                "password2": password,
                "account_type": AccountType.STUDENT.value
                if student
                else AccountType.TUTOR.value,
            },
            follow=True,
        )

    def _login_user(self, username: str, password: str = "haslo123") -> None:
        """Log the user in.

        The method logs the user in by sending a
        request to the `profiles:login` page.
        The method could be used instead of default
        'self.client.login' in cases where the value of
        the 'account_type' session must be set. The
        setting of that value is done in the login
        view.

        Args:
            username: Username of the user is meant to be
                        logged in.
            password: Password of the user that is meant to
                        be logged in.
        """
        self.client.post(
            reverse("profiles:login"),
            {
                "username": username,
                "password": password,
            },
        )
