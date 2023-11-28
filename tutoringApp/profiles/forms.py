"""Forms for logging and registering users."""

from enum import Enum, auto
from pathlib import Path

from django import forms
from django.contrib.auth.forms import (
    AuthenticationForm,
    UserCreationForm,
    UsernameField,
)
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _

from profiles.models import Education, Profile, ProfileLanguageList, Service


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
    username = UsernameField(
        min_length=5,
        max_length=150,
        error_messages={"unique": "Username already taken."},
    )
    email = forms.EmailField(
        required=True, error_messages={"unique": "Email already taken."}
    )
    first_name = forms.CharField(max_length=150, required=True)
    last_name = forms.CharField(max_length=150, required=True)

    class Meta:
        model = User
        model._meta.get_field("email")._unique = True
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


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = [
            "user",
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
            "teaching_since": forms.DateInput(
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

    def clean(self) -> None:
        """Additional validation of start_- and end_- date fields.

        The method validates that start_date falls BEFORE
        end_date. If not, ValidationErrors are added to
        both fields.
        """
        cleaned_data = super().clean()
        start_date = cleaned_data.get("start_date")
        end_date = cleaned_data.get("end_date")

        if start_date and end_date:
            if start_date > end_date:
                validation_error = ValidationError(
                    _("Start date: %(start_date)s falls after End date: %(end_date)s"),
                    code="invalid",
                    params={"start_date": start_date, "end_date": end_date},
                )
                self.add_error("start_date", validation_error)
                self.add_error("end_date", validation_error)


education_formset = forms.inlineformset_factory(
    parent_model=Profile,
    model=Education,
    form=EducationForm,
    extra=1,
    can_delete=True,
    can_delete_extra=False,
    min_num=0,
    validate_min=False,
)


class ProfileLanguageListForm(forms.ModelForm):
    """Form for inputting language information.

    The form is used on the page for creating/updating Tutor's profile
    to allow them to state which languages they speak and which of them
    can be used during a tutoring session. The form is rendered in a
    formset (profile_language_list_formset) and at least one correct form
    must be submitted.
    """

    class Meta:
        model = ProfileLanguageList
        exclude = ["profile"]

        widgets = {
            "language": forms.Select(attrs={"class": "options"}),
            "level": forms.Select(attrs={"class": "options"}),
        }


profile_language_list_formset = forms.inlineformset_factory(
    parent_model=Profile,
    model=ProfileLanguageList,
    form=ProfileLanguageListForm,
    extra=1,
    can_delete=True,
    can_delete_extra=False,
    min_num=1,
    validate_min=True,
    error_messages={"too_few_forms": "You must input at least one language!"},
)


class SubjectForm(forms.ModelForm):
    """Form for inputting initial about subject taught by a given Tutor.

    The form is used on the page for creating/updating Tutor's profile
    which means that only basic information (subject, price per hour and
    session length) are required. The values of other fields are set
    to model's default values. In particular the 'is_default' field
    is set to True  which means that a one-time session for given subject is
    always available. The form is rendered in a formset (subject_formset)
    and at least one correct form must be submitted.
    """

    class Meta:
        model = Service
        exclude = ["tutor", "number_of_hours", "is_default"]

        SESSION_LENGTH_CHOICES = [
            (length, str(length)) for length in range(30, 181, 15)
        ]

        widgets = {
            "subject": forms.Select(attrs={"class": "options"}),
            "price_per_hour": forms.NumberInput(attrs={"class": "number-input"}),
            "session_length": forms.Select(
                attrs={"class": "options"}, choices=SESSION_LENGTH_CHOICES
            ),
        }


subject_formset = forms.inlineformset_factory(
    parent_model=Profile,
    model=Service,
    form=SubjectForm,
    extra=1,
    can_delete=True,
    can_delete_extra=False,
    min_num=1,
    validate_min=True,
    error_messages={"too_few_forms": "You must input at least one subject!"},
)
