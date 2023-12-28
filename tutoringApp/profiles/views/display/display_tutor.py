"""Views for displaying Tutors' profile information."""
from collections import OrderedDict
from datetime import datetime
from typing import Any, Literal

from django.conf import settings
from django.db.models.query import QuerySet
from django.http import HttpRequest, HttpResponse
from pandas import Timestamp, date_range

from profiles.forms import AccountType
from profiles.models import ProfileLanguageList
from tutors.models import Availability, Service

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

        context["availabilites"] = self._get_availabilites()

        context["current_week"] = self._get_dates_for_week(
            self._get_week_days("current")
        )

        context["week_days_dates"] = self._get_week_days_dates()

        context["default_services"] = Service.objects.filter(
            tutor=self.get_object()
        ).filter(is_default=True)

        context["first_service"] = context["default_services"][0]
        context["current_month"] = datetime.now().month
        context["current_year"] = datetime.now().year

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

    @staticmethod
    def _get_week_days(week: Literal["previous", "current", "next"]) -> list[Timestamp]:
        """Get days of past, next or current week.

        Args:
            week: String flag indicating the week
                for which dates of days should be
                returned.

        Returns:
            A list containing pandas's Timestamp,
            each representing different day of
            the past, previous or next week.
        """
        week_offset_mapping = {"previous": -1, "current": 0, "next": 1}
        date_now = datetime.now()
        date_start = f"{date_now.year}-W{date_now.isocalendar().week + week_offset_mapping[week]}-1"
        date_end = f"{date_now.year}-W{date_now.isocalendar().week + week_offset_mapping[week]}-0"
        return date_range(
            start=datetime.strptime(date_start, "%Y-W%W-%w"),
            end=datetime.strptime(date_end, "%Y-W%W-%w"),
        )

    def _get_availabilites(self) -> dict[Service, list[QuerySet]]:
        """Get availiablity for the current week.

        The method fetches every Availability object
        related to a default Service (Service with `1` as the
        value of `number_of_hours` field) for the current week.

        Returns:
            A dictionary with keys being Service objects' PKs
            (Service objects are related to the currently displayed
            tutor) and the values of lists storing 7 QuerySets,
            each with `Availability` objects defined for different
            days of the current week.
        """
        services = Service.objects.filter(tutor=self.get_object()).filter(
            is_default=True
        )
        availabilites = {}
        for service in services:
            availabilites_service = {}
            for week in ["previous", "current", "next"]:
                availabilites_service.update(
                    {
                        week: [
                            Availability.objects.filter(service=service).filter(
                                start__year=date.year,
                                start__month=date.month,
                                start__day=date.day,
                                booking__pk=None,
                            )
                            for date in self._get_week_days(week)
                        ]
                    }
                )
            availabilites.update({service: availabilites_service})
        return availabilites

    def _get_current_dates(self) -> dict[str,]:
        """Return dates to be rendered in the template.

        Returns:
            A dictionary with keys being names of days of week
            and values being th actual dates of these days.
        """
        week = {}
        current_week = self._get_week_days("current")
        for day in current_week:
            week.update({day.date().strftime("%a"): day.date().strftime("%d. %b")})
        return week

    @staticmethod
    def _get_dates_for_week(week_range: list[Timestamp]) -> dict[str, str]:
        """Return dates to be rendered in the template.

        Args:
            week_range: A list with Timestaps representing
                        dates of days in a given week.

        Returns:
            A dictionary with keys being names of days of week
            and values being th actual dates of these days from
            a given week.
        """
        week = {}
        for day in week_range:
            week.update({day.date().strftime("%a"): day.date().strftime("%d. %b")})
        return week

    def _get_week_days_dates(self) -> dict[str, dict[str, str]]:
        """Return dates of days from previous, current and next week.

        The values contained in the dictionary will be
        rendered in the template.

        Returns:
            A dictionary where keys are string indicating the week
            (previous, current or next) and values are dictionaries
            with keys being names of days of week and values being the actual
            dates of these days from a given week.
        """
        week_days_dates = OrderedDict()
        for week in ["previous", "current", "next"]:
            week_days_dates.update(
                {week: self._get_dates_for_week(self._get_week_days(week))}
            )
        return week_days_dates
