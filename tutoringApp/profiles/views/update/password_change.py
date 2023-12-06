from logging import getLogger
from typing import Any

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordChangeView as AuthPasswordChangeView
from django.http import HttpResponse
from django.urls import reverse

LOGGER = getLogger(__name__)


class PasswordChangeView(AuthPasswordChangeView, LoginRequiredMixin):
    """View for changing the currently logged in user's password."""

    template_name = "profiles/change_password.html"

    def get_success_url(self) -> str:
        """Redirect the user to their profile."""
        return reverse("profiles:student_display", kwargs={"pk": self.request.user.id})

    def form_invalid(self, form: Any) -> HttpResponse:
        """Invoked when the form data is incorrect."""
        LOGGER.debug(
            f"Password of user user with id {self.request.user.id} not updated due to following errors: {form.errors}"
        )
        return super().form_invalid(form)

    def form_valid(self, form: Any) -> HttpResponse:
        """Invoked when the form data is correct."""
        LOGGER.debug(
            f"Correctly updated the password of the user with id {self.request.user.id}"
        )
        return super().form_valid(form)
