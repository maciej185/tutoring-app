"""Views for the `learning_tutor` page."""
from logging import getLogger
from typing import Any, Optional

from django.db.models.query import QuerySet
from django.http import HttpRequest, HttpResponse
from django.http.request import HttpRequest
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.generic.edit import ProcessFormView

from subscriptions.forms import ServiceSubscriptionListForm
from subscriptions.models import ServiceSubscriptionList, Subscription

from .learning import LearningView

LOGGER = getLogger(__name__)


class LearningTutorView(LearningView, ProcessFormView):
    """Display Lessons of Students subscribed to given Tutor.

    The view displays a list of Lesson objects are
    related to Appointment created for a given Subscription
    whose primary key has been passed as the URL parameter.
    The view also allows to create new Subscription objects
    with other other Students by rendering an appropriate form.
    """

    template_name = "subscriptions/learning/tutor.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        """Add data to the default context."""
        context = super().get_context_data(**kwargs)
        context["subscriptions"] = self._get_subscriptions()
        context["service_subscription_list_form"] = ServiceSubscriptionListForm(
            initial={"subscription": self.subscription}
        )

        return context

    def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        """Process data sent via ServiceSubscriptionListForm."""
        user_not_tutor_warning_response = self._user_not_tutor_warning_response()
        if user_not_tutor_warning_response:
            return user_not_tutor_warning_response
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
        user_not_tutor_warning_response = self._user_not_tutor_warning_response()
        return (
            user_not_tutor_warning_response
            if user_not_tutor_warning_response
            else super().get(request, *args, **kwargs)
        )

    def _get_subscriptions(self) -> QuerySet[Subscription]:
        """Get all Subscriptions related to the current Tutor.

        Returns:
            A QuerySet with all Subscriptions objects
            related to the currently logged in Tutor.
        """
        return Subscription.objects.filter(tutor__user=self.request.user)

    def _user_not_tutor_warning_response(self) -> Optional[HttpResponse]:
        """Check if the currently logged in user is the Tutor related to the Subscription.

        Returns:
            An instance of the HttpResponse which renders a
            page with a warning message if the currently
            logged in user is not the Tutor related to the
            the Subscription object that is meant to be displayed.
        """
        if self.request.user != self.subscription.tutor.user:
            LOGGER.warning(
                "User %(username)s with ID %(id)s attempting to display learining page of Tutor with ID %(tutor_id)s.",
                {
                    "username": self.request.user.username,
                    "id": self.request.user.id,
                    "tutor_id": self.subscription.tutor.pk,
                },
            )
            return render(
                request=self.request,
                template_name="tutoringApp/forbidden.html",
                status=403,
                context={
                    "warning_message": "You are not allowed to access this page.",
                    "redirect_link": reverse("home:home"),
                    "redirect_destination": "home page",
                },
            )
