"""Forms for logging and registering users."""

from pathlib import Path

from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User


class LoginForm(AuthenticationForm):
    """Subclass already implented login form to change the appearance."""

    error_messages = {
        "invalid_login": "Username or password are incorrect.",
        "inactive": "Account is inactive.",
    }

    template_name_div = Path("profiles", "login_form_div.html")

    widgets = {"username": forms.TextInput(attrs={"class": "text-input"})}


class RegisterForm(UserCreationForm):
    account_type = forms.ChoiceField(
        choices=[(0, "Student"), (1, "Tutor")], required=True
    )
    username = forms.CharField(min_length=5, max_length=150)
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = (
            "username",
            "first_name",
            "last_name",
            "email",
            "password1",
            "password2",
        )

        labels = {
            "username": "Username",
            "first_name": "First name",
            "last_name": "Last name",
            "email": "Email address",
            "password1": "Password",
            "password2": "Cofnirm password",
            "account_type": "Account type",
        }

        widgets = {
            "username": forms.TextInput(attrs={'class': 'text-input'}),
            "first_name": forms.TextInput(attrs={'class': 'text-input'}),
            "last_name": forms.TextInput(attrs={'class': 'text-input'}),
            "email": forms.EmailInput(attrs={'class': 'text-input'}),
            "password1": forms.PasswordInput(attrs={'class': 'text-input'}),
            "password2": forms.PasswordInput(attrs={'class': 'text-input'}),
            "account_type": forms.CheckboxInput(attrs={'class': 'options'}),
            }

    template_name_div = Path("profiles", "register_form_div.html")
