import calendar
import datetime
from collections import OrderedDict
from logging import getLogger
from typing import Any

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.db.models.query import QuerySet
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.generic.detail import DetailView

from profiles.models import Profile
from tutors.models import Availability, Service

LOGGER = getLogger(__name__)


class AvailabilityInputView(DetailView, LoginRequiredMixin):
    template_name = "tutors/availability_input.html"
    model = Service

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)

        context["availabilites"] = self._get_availabilites()

        context["services"] = Service.objects.filter(
            tutor=self.get_object().tutor
        ).filter(is_default=True)

        context["calendar_grid"] = self._get_calendar_grid()

        context["month_index"] = self.kwargs["month"]

        context["month_name"] = calendar.month_name[self.kwargs["month"]]

        context["year_index"] = self.kwargs["year"]

        context["current_service_id"] = self.kwargs["pk"]

        return context

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        """Check if the currently logged in user is configured as tutor in given Service object."""
        profile = Profile.objects.get(user=request.user)
        if profile != self.get_object().tutor:
            LOGGER.warning(
                "User %(username)s with id %(id)s attempting to configure services of %(service_tutor)s with id %(service_tutor_id)s!",
                {
                    "username": self.request.user.username,
                    "id": self.request.user.id,
                    "profile_owner": User.objects.get(
                        pk=self.get_object().tutor.pk
                    ).username,
                    "profile_owner_id": self.get_object().tutor.pk,
                },
            )
            return render(
                request=request,
                template_name="tutoringApp/forbidden.html",
                status=403,
                context={
                    "warning_message": "You are not allowe to configure tutor's services!",
                    "redirect_link": reverse("home:home"),
                    "redirect_destination": "home page",
                },
            )

        return super().get(request, *args, **kwargs)

    def _get_calendar_grid(self) -> dict[int, str]:
        """Returna dictionary used to render current month's grid.

        Returns:
            Dictionary with at most 42 elements, each referring to one cell
            in a calendar grid.
        """
        calendar_grid_dict = OrderedDict()

        now = datetime.datetime.now()
        month_calendar = calendar.monthcalendar(
            self.kwargs["year"], self.kwargs["month"]
        )

        previous_months_days_count = month_calendar[0].count(0)
        next_months_days_count = month_calendar[-1].count(0)

        previous_months_year = (
            self.kwargs["year"]
            if self.kwargs["month"] - 1 != 0
            else self.kwargs["year"] - 1
        )
        previous_months_index = (
            self.kwargs["month"] - 1 if self.kwargs["month"] - 1 != 0 else 12
        )

        # next_months_year = self.kwargs["year"] if self.kwargs["month"] + 1 != 13 else self.kwargs["year"] + 1
        next_months_index = (
            self.kwargs["month"] + 1 if self.kwargs["month"] + 1 != 13 else 1
        )

        previous_months_days = list(
            range(
                1,
                calendar.monthrange(previous_months_year, previous_months_index)[1] + 1,
            )
        )
        previous_months_days.reverse()

        for i in reversed(range(previous_months_days_count)):
            calendar_grid_dict.update(
                {
                    str(previous_months_index)
                    + "_"
                    + str(previous_months_days[i]): "not_current"
                }
            )

        for i in range(
            1, calendar.monthrange(self.kwargs["year"], self.kwargs["month"])[1] + 1
        ):
            calendar_grid_dict.update({i: "current"})

        for i in range(1, next_months_days_count + 1):
            calendar_grid_dict.update(
                {str(next_months_index) + "_" + str(i): "not_current"}
            )

        calendar_grid_dict_with_placeholders = OrderedDict()
        calendar_grid_dict_with_placeholders.update({"placeholder_0": "placeholder"})

        i = 1
        for day in calendar_grid_dict:
            if i % 7 == 0:
                calendar_grid_dict_with_placeholders.update(
                    {day: calendar_grid_dict[day]}
                )
                calendar_grid_dict_with_placeholders.update(
                    {f"placeholder_{i}": "placeholder"}
                )
                calendar_grid_dict_with_placeholders.update(
                    {f"placeholder_{i + 1}": "placeholder"}
                )
            else:
                calendar_grid_dict_with_placeholders.update(
                    {day: calendar_grid_dict[day]}
                )
            i += 1

        calendar_grid_dict_with_placeholders.update({f"placeholder_{i}": "placeholder"})

        return calendar_grid_dict_with_placeholders

    def _get_availabilites(self) -> list[QuerySet]:
        """Return a list with Availability objects for given month.

        Returns:
            List containing availability QuerySets, each corresponding
            to one day of the given month.
        """
        days_in_month = calendar.monthrange(self.kwargs["year"], self.kwargs["month"])[
            1
        ]
        return [
            Availability.objects.filter(service=self.get_object()).filter(
                start__year=self.kwargs["year"],
                start__month=self.kwargs["month"],
                start__day=i,
            )
            for i in range(1, days_in_month + 1)
        ]
