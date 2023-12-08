"""Views for resetting a password."""
from django.contrib.auth.views import (
    PasswordResetCompleteView,
    PasswordResetConfirmView,
    PasswordResetDoneView,
    PasswordResetView,
)
from django.urls import reverse_lazy


class ProfilesPasswordResetView(PasswordResetView):
    template_name = "password_reset/password_reset.html"
    success_url = reverse_lazy("profiles:password_reset_done")
    email_template_name = "password_reset/password_reset_email.html"
    subject_template_name = "password_reset/password_reset_subject.txt"


class ProfilesPasswordResetDoneView(PasswordResetDoneView):
    template_name = "password_reset/password_reset_done.html"


class ProfilesPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = "password_reset/password_reset_confirm.html"
    success_url = reverse_lazy("profiles:password_reset_complete")


class ProfilesPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = "password_reset/password_reset_complete.html"
