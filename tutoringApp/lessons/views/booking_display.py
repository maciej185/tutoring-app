"""Views for displaying a list of Booking objects."""
from typing import Any

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.db.models.query import QuerySet
from django.views.generic.list import ListView

from lessons.models import Booking
from profiles.models import Profile
from tutors.models import Service


class BookingsDisplay(ListView, LoginRequiredMixin):
    """Display booking objects."""

    model = Booking
    paginate_by = 5


class BookingsDisplay4Student(BookingsDisplay):
    """Display booking objects for a Student."""

    template_name = "booking/display_4_student.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        """Include additional context variables."""
        context = super().get_context_data(**kwargs)
        context["profile_filter_list"] = self._get_profile_filter_list()
        return context

    def _get_profile_filter_list(self) -> QuerySet[Profile]:
        """Get a list of Profile objects for filtering.

        Returns:
            Get a list of Profiles that the list of Bookings could be filtered by.
        """
        services = Service.objects.filter(
            availability__booking__student=Profile.objects.get(user=self.request.user)
        )
        return [*{*[service.tutor for service in services]}]

    def get_queryset(self) -> QuerySet[Booking]:
        """Filter Booking objects assigned to a given Student.

        Returns:
            A QuerySet with Booking objects related to the currently logged in Student.
        """
        filters = [
            Q(availability__start__date__gte=self.request.GET.get("from", None))
            if self.request.GET.get("from", None)
            else None,
            Q(availability__start__date__lte=self.request.GET.get("to", None))
            if self.request.GET.get("to", None)
            else None,
            Q(availability__service__tutor__pk=self.request.GET.get("profile", None))
            if self.request.GET.get("profile", None)
            else None,
        ]
        filters = filter(lambda x: x, filters)
        return Booking.objects.filter(
            student=Profile.objects.get(user=self.request.user),
            *filters
        ).order_by("-availability__start")