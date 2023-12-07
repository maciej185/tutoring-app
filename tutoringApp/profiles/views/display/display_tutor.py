"""Views for displaying Tutors' profile information."""
from typing import Any

from django.conf import settings
from django.http import HttpRequest, HttpResponse

from profiles.forms import AccountType
from profiles.models import ProfileLanguageList, Service

from .display import DisplayProfileView


class DisplayTutorProfileView(DisplayProfileView):
    """Display Students' profile information."""

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        """Add info about Service and ProfileLanguageList objects related to given Tutor."""
        context = super().get_context_data(**kwargs)

        context["language_data"] = ProfileLanguageList.objects.filter(
            profile=self.get_object()
        )

        context["service_data"] = Service.objects.filter(tutor=self.get_object())

        context["currency"] = settings.CURRENCY

        subjects = list(
            set(
                [
                    service_object.subject.name
                    for service_object in context["service_data"]
                ]
            )
        )

        context["subject_list"] = (
            (
                "".join(
                    [
                        f"{subject}, "
                        for ind, subject in enumerate(subjects)
                        if ind != len(subjects) - 1
                    ]
                )
                + subjects[-1]
            )
            if subjects
            else ""
        )

        return context

    def get_template_names(self) -> str:
        """Decide which template to display based on the current user's profile type."""
        account_type = self.request.session.get("account_type")
        return (
            "profiles/display_tutor_4_tutor.html"
            if account_type == AccountType.TUTOR.value
            else "profiles/display_tutor_4_student.html"
        )

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        """Ensure that the profile exists and correct page is displayed."""
        if self._pofile_does_not_exist_redirect():
            return self._pofile_does_not_exist_redirect()
        incorrect_display_type_redirect = self._incorrect_display_page_for_type(
            self.kwargs["pk"], display_type_is_student=False
        )
        return (
            incorrect_display_type_redirect
            if incorrect_display_type_redirect
            else super().get(request, *args, **kwargs)
        )
