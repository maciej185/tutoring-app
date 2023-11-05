"""Forms for logging and registering users."""

from django.contrib.auth.forms import AuthenticationForm
from pathlib import Path
from django import forms

class LoginForm(AuthenticationForm):
    """Subclass already implented login form to change the appearance."""

    error_messages = {
        "invalid_login": "Username or password are incorrect.",
        "inactive": "Account is inactive.",
    }

    template_name_div = Path("profiles", "login_form_div.html")

    widgets = {
            'username': forms.TextInput(attrs={'class': 'text-input'})
        }


