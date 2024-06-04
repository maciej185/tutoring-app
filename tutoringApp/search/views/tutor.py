"""View for generating search results for Tutors."""
from typing import Any

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models.functions import Lower
from django.db.models.query import QuerySet
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.views.generic.list import ListView

from profiles.forms import AccountType
from profiles.models import Profile


class TutorSearchResultsView(ListView, LoginRequiredMixin):
    """View for generating search results for Tutors."""

    model = Profile
    paginate_by = 10
    template_name = r"search\tutor.html"

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        if request.session.get("account_type") == AccountType.STUDENT.value:
            return HttpResponseRedirect(request.get_full_path_info().replace("tutor", "student"))
        return super().get(request, *args, **kwargs)

    def get_queryset(self) -> QuerySet[Profile]:
        """Filter the search results based on query parameters."""
        search_first_name = self.request.GET.get("first_name", None)
        search_last_name = self.request.GET.get("last_name", None)
        students = (
            Profile.objects.annotate(
                first_name_lower=Lower("user__first_name"), last_name_lower=Lower("user__last_name")
            )
            .filter(teaching_since__isnull=True)
            .distinct()
        )
        if search_first_name:
            students = students.filter(first_name_lower__contains=search_first_name.lower())
        if search_last_name:
            students = students.filter(last_name_lower__contains=search_last_name.lower())
        return students
