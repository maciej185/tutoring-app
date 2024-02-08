"""Base view for the `learning_tutor` and `learning_student` pages."""

from typing import Any

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import QuerySet
from django.http import HttpRequest
from django.utils.timezone import now
from django.views.generic.list import ListView

from lessons.models import Lesson
from subscriptions.models import Appointment, ServiceSubscriptionList, Subscription


class LearningView(ListView, LoginRequiredMixin):
    """Display Lessons under a given Subscription."""

    model = Appointment
    paginate_by = 5

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.subscription = None

    def setup(self, request: HttpRequest, *args: Any, **kwargs: Any) -> None:
        """Assign current Subscription to an attribute."""
        super().setup(request, *args, **kwargs)
        self.subscription = Subscription.objects.get(pk=self.kwargs["subscription_id"])

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        """Add data to the default context."""
        context = super().get_context_data(**kwargs)
        context["hours_left"] = self._calculate_hours_left()
        context["hours_used"] = self._calculate_hours_total() - context["hours_left"]
        context["current_subscription"] = self.subscription
        context["now"] = now()

        return context

    def _calculate_hours_total(self) -> int:
        """Calculate total hour count.

        Returns:
            Total hour count calculated based on
            all purchased Services, information on which
            is stored in the ServiceSubscriptionList table.
        """
        return sum(
            [
                service_subscription.service.number_of_hours
                for service_subscription in ServiceSubscriptionList.objects.filter(
                    subscription=self.subscription
                )
            ]
        )

    def _calculate_hours_left(self) -> int:
        """Calculate available hour count.

        Returns:
            Available hours in a given Subscription
            calculated by substracting the number of
            all related Lesson objects from the number
            of total hours purchased, calculated based on the
            fetched ServiceSubscriptionList objects.
        """
        return self._calculate_hours_total() - len(self.get_queryset())

    def get_queryset(self) -> QuerySet[Lesson]:
        """Get only Lessons related to given Subscription."""
        service_subscription_lists = ServiceSubscriptionList.objects.filter(
            subscription=self.subscription,
            service__tutor=self.subscription.tutor,
        )
        appointments = []
        for service_subscription_list in service_subscription_lists:
            appointments.extend(service_subscription_list.appointment_set.all())
        return appointments
