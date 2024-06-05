"""View for generating search results for Students."""
from math import floor
from typing import Any

from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.db.models.functions import Lower
from django.db.models.query import QuerySet
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.views.generic.list import ListView

from profiles.forms import AccountType
from profiles.models import Profile
from tutors.models import Service, Subject


class StudentSearchResultsView(ListView, LoginRequiredMixin):
    """View for generating search results for Students."""

    model = Profile
    paginate_by = 10
    template_name = "search\student.html"

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        """Ensure that correct page for given account type is displayed.

        In case that the logged in user is a Tutor, they get redirected to
        a page with search results for Tutors while preserving the query
        parameters provided in the initial request.
        """
        if request.session.get("account_type") == AccountType.TUTOR.value:
            return HttpResponseRedirect(request.get_full_path_info().replace("student", "tutor"))
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        """Add additional information to the context."""
        profiles = self.get_queryset()
        context = super().get_context_data(**kwargs)

        context["subjects"] = [self._get_subjects(profile) for profile in profiles]
        context["average_prices"] = [self._get_average_price(profile) for profile in profiles]
        context["currency"] = settings.CURRENCY
        context["search_subject"] = (
            Subject.objects.get(pk=self.request.GET.get("subject", None))
            if self.request.GET.get("subject", None)
            else None
        )
        return context

    def get_queryset(self) -> QuerySet[Any]:
        """Filter the search results based on query parameters."""
        search_subject = self.request.GET.get("subject", None)
        search_first_name = self.request.GET.get("first_name", None)
        search_last_name = self.request.GET.get("last_name", None)
        tutors = (
            Profile.objects.annotate(
                first_name_lower=Lower("user__first_name"), last_name_lower=Lower("user__last_name")
            )
            .filter(teaching_since__isnull=False)
            .distinct()
        )
        if search_first_name:
            tutors = tutors.filter(first_name_lower__contains=search_first_name.lower())
        if search_last_name:
            tutors = tutors.filter(last_name_lower__contains=search_last_name.lower())
        if search_subject:
            tutors = tutors.filter(service__subject=search_subject)
        return tutors

    def _get_subjects(self, tutor: Profile) -> list[str]:
        """Return an arrya with the names of Subjects taught by the given Tutor."""
        return list(set([service.subject.name for service in Service.objects.filter(tutor=tutor)]))

    def _get_average_price(self, tutor: Profile) -> int:
        """Return average price of services offered by the given Tutor."""
        services = Service.objects.filter(tutor=tutor)
        return floor(sum([service.price_per_hour for service in services]) / len(services))
