"""Views for displaying the profile objects."""

from typing import Any, Optional

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic.detail import DetailView

from profiles.models import Education, Profile


class DisplayProfileView(DetailView, LoginRequiredMixin):
    """Display profile information."""

    model = Profile

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        """Add education and user data to the default context."""
        context = super().get_context_data(**kwargs)

        context["education_data"] = Education.objects.filter(profile=self.get_object())

        context["profile_user"] = User.objects.get(pk=self.kwargs["pk"])

        return context

    @staticmethod
    def _incorrect_display_page_for_type(
        profile_id: int, display_type_is_student: bool
    ) -> Optional[HttpResponseRedirect]:
        """Check if the current display page matches the type of the profile.

        The method checks the type of the Profile object whos
        primary key has been sent as part of the URL. If the type
        of the desired profile does not match the type of the
        display page, a redirection link is returned.

        Args:
            profile_id: Primary key of the `Profile` object
                        that is meant to be displayed.
            display_type_is_student: Boolean information about whether
                                    the current view displays a page
                                    with Student's profile information.
        Return:
            Instance of the HttpResponseRedirect class if the type
            of display profile page does not match the type of the profile,
            None otherwise.
        """
        profile = Profile.objects.get(pk=profile_id)
        if display_type_is_student:
            if not profile.is_student():
                return HttpResponseRedirect(
                    reverse("profiles:tutor_display", kwargs={"pk": profile_id})
                )
        else:
            if profile.is_student():
                return HttpResponseRedirect(
                    reverse("profiles:student_display", kwargs={"pk": profile_id})
                )
