"""Views for displaying Students' profile information."""
from typing import Any

from django.http import HttpRequest, HttpResponse

from profiles.forms import AccountType

from .display import DisplayProfileView


class DisplayStudentProfileView(DisplayProfileView):
    """Display Students' profile information."""

    def get_template_names(self) -> list[str]:
        """Decide which template to display based on the current user's profile type."""
        account_type = self.request.session.get("account_type")
        return (
            "profiles/display_student_4_tutor.html"
            if account_type == AccountType.TUTOR.value
            else "profiles/display_student_4_student.html"
        )

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        """Ensure that the profile exists and correct page is displayed."""
        if self._pofile_does_not_exist_redirect():
            return self._pofile_does_not_exist_redirect()
        incorrect_display_type_redirect = self._incorrect_display_page_for_type(
            self.kwargs["pk"], display_type_is_student=True
        )
        return (
            incorrect_display_type_redirect
            if incorrect_display_type_redirect
            else super().get(request, *args, **kwargs)
        )
