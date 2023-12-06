"""Views for displaying the profile objects."""

from typing import Any

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
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
