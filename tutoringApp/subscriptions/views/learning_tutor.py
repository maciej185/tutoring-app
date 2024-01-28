"""Views for the `learning_tutor` page."""
from logging import getLogger
from typing import Any

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models.query import QuerySet
from django.http import HttpRequest, HttpResponse
from django.http.request import HttpRequest
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.generic.edit import ProcessFormView
from django.views.generic.list import ListView

from lessons.models import Lesson
from profiles.models import Profile
from subscriptions.forms import ServiceSubscriptionListForm
from subscriptions.models import ServiceSubscriptionList, Subscription

LOGGER = getLogger(__name__)


class LearningTutorView(ListView, ProcessFormView, LoginRequiredMixin):
    """Display Lessons of Students subscribed to given Tutor.

    The view displays a list of Lesson objects are
    related to Appointment created for a given Subscription
    whose primary key has been passed as the URL parameter.
    The view also allows to create new Subscription objects
    with other other Students by rendering an appropriate form.
    """

    model = Lesson
    paginate_by = 5
    template_name = "subscriptions/learning/tutor.html"

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
        context["subscriptions"] = self._get_subscriptions()
        context["current_subscription"] = self.subscription
        context["service_subscription_list_form"] = ServiceSubscriptionListForm(
            initial={"subscription": self.subscription}
        )

        return context

    def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        """Process data sent via ServiceSubscriptionListForm."""
        service_subscription_list_form = ServiceSubscriptionListForm(
            request.POST, initial={"subscription": self.subscription}
        )
        if service_subscription_list_form.is_valid():
            service_subscription_list = ServiceSubscriptionList(
                subscription=self.subscription,
                service=service_subscription_list_form.cleaned_data["service"],
            )
            service_subscription_list.save()
            return HttpResponseRedirect(
                reverse(
                    "subscriptions:learning_tutor",
                    kwargs={"subscription_id": self.kwargs["subscription_id"]},
                )
            )
        return super().post(request, *args, **kwargs)

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        """Ensure the user is the Tutor related to given Subscription."""
        if request.user != self.subscription.tutor.user:
            LOGGER.warning(
                "User %(username)s with ID %(id)s attempting to display learining page of Tutor with ID %(tutor_id)s.",
                {
                    "username": self.request.user.username,
                    "id": self.request.user.id,
                    "tutor_id": self.subscription.tutor.pk,
                },
            )
            return render(
                request=request,
                template_name="tutoringApp/forbidden.html",
                status=403,
                context={
                    "warning_message": "You are not allowed to view this page.",
                    "redirect_link": reverse("home:home"),
                    "redirect_destination": "home page",
                },
            )
        return super().get(request, *args, **kwargs)

    def get_queryset(self) -> QuerySet[Lesson]:
        """Get only Lessons related to given Subscription."""
        service_subscription_lists = ServiceSubscriptionList.objects.filter(
            subscription=self.subscription,
            service__tutor=Profile.objects.get(user=self.request.user),
        )
        appointments = []
        for service_subscription_list in service_subscription_lists:
            appointments.extend(service_subscription_list.appointment_set.all())
        return [appointment.lesson_info for appointment in appointments]

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

    def _get_subscriptions(self) -> QuerySet[Subscription]:
        """Get all Subscriptions related to the current Tutor.

        Returns:
            A QuerySet with all Subscriptions objects
            related to the currently logged in Tutor.
        """
        return Subscription.objects.filter(tutor__user=self.request.user)
