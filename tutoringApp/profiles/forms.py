"""Forms for logging and registering users."""

from enum import Enum, auto
from pathlib import Path

from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User

from profiles.models import Education, Profile


class AccountType(Enum):
    """Simple enum class for specifying account's type."""

    STUDENT = auto()
    TUTOR = auto()


class AccountType(Enum):
    """Simple enum class for specifying account's type."""

    STUDENT = auto()
    TUTOR = auto()


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
        choices=[
            (AccountType.STUDENT.value, "Student"),
            (AccountType.TUTOR.value, "Tutor"),
        ],
        required=True,
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
            "username": forms.TextInput(attrs={"class": "text-input"}),
            "first_name": forms.TextInput(attrs={"class": "text-input"}),
            "last_name": forms.TextInput(attrs={"class": "text-input"}),
            "email": forms.EmailInput(attrs={"class": "text-input"}),
            "password1": forms.PasswordInput(attrs={"class": "text-input"}),
            "password2": forms.PasswordInput(attrs={"class": "text-input"}),
            "account_type": forms.CheckboxInput(attrs={"class": "options"}),
        }

    template_name_div = Path("profiles", "register_form_div.html")


class UpdateUserForm(forms.ModelForm):
    first_name = forms.CharField(max_length=100, required=True)
    last_name = forms.CharField(max_length=100, required=True)
    email = forms.EmailField(max_length=100, required=True)

    class Meta:
        model = User
        fields = ["first_name", "last_name", "email"]


class StudentProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = [
            "user",
            "teaching_since",
            "create_date",
            "timestamp",
            "languages",
            "schools",
        ]

        widgets = {
            "profile_pic": forms.FileInput(
                attrs={"id": "profile-info-main-left_top-picture-input-input"}
            ),
            "date_of_birth": forms.DateInput(
                format=("%Y-%m-%d"),
                attrs={"type": "date"},
            ),
        }


class EducationForm(forms.ModelForm):
    class Meta:
        model = Education
        exclude = ["profile"]

        widgets = {
            "school": forms.Select(attrs={"class": "education-form-school"}),
            "start_date": forms.DateInput(
                format=("%Y-%m-%d"),
                attrs={"class": "education-form-start_date", "type": "date"},
            ),
            "end_date": forms.DateInput(
                format=("%Y-%m-%d"),
                attrs={"class": "education-form-end_date", "type": "date"},
            ),
            "degree": forms.TextInput(attrs={"class": "education-form-degree"}),
            "additional_info": forms.TextInput(
                attrs={"class": "education-form-additional_info"}
            ),
        }


education_formset = forms.inlineformset_factory(
    parent_model=Profile,
    model=Education,
    form=EducationForm,
    extra=1,
    can_delete=False,
    can_delete_extra=False,
    min_num=0,
    validate_min=False,
)
