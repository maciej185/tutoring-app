"""Forms for logging and registering users."""

from django.contrib.auth.forms import AuthenticationForm


class LoginForm(AuthenticationForm):
    """Subclass already implented login form to change error messages."""

    error_messages = {
        "invalid_login": "Username or password are incorrect.",
        "inactive": "Account is inactive.",
    }
