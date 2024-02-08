"""Views for the `appointment_delete` page."""

from logging import getLogger
from typing import Any, Optional

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.generic.edit import DeleteView

from subscriptions.models import Appointment, ServiceSubscriptionList

LOGGER = getLogger(__name__)


class DeleteAppointmentView(DeleteView):
    """View for deleting Appointment objects."""

    model = Appointment
    template_name = "subscriptions/appointment_delete.html"

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.subscription = None

    def setup(self, request: HttpRequest, *args: Any, **kwargs: Any) -> None:
        super().setup(request, *args, **kwargs)
        self.subscription = ServiceSubscriptionList.objects.get(
            appointment=self.get_object()
        ).subscription

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        user_not_tutor_warning_response = self._user_not_tutor_warning_response()
        return (
            user_not_tutor_warning_response
            if user_not_tutor_warning_response
            else super().get(request, *args, **kwargs)
        )

    def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        user_not_tutor_warning_response = self._user_not_tutor_warning_response()
        return (
            user_not_tutor_warning_response
            if user_not_tutor_warning_response
            else super().post(request, *args, **kwargs)
        )

    def form_valid(self, *args, **kwargs):
        """Delete the realated `Lesson` object."""
        self.get_object().lesson_info.delete()
        return super().form_valid(*args, **kwargs)

    def get_success_url(self) -> str:
        """Redirect Tutor back to the `learning_tutor` page."""
        return reverse(
            "subscriptions:learning_tutor",
            kwargs={"subscription_id": self.subscription.pk},
        )

    def _user_not_tutor_warning_response(self) -> Optional[HttpResponse]:
        """Check if the currently logged in user is the Tutor related to the Appointment.

        Returns:
            An instance of the HttpResponse which renders a
            page with a warning message if the currently
            logged in user is not the Tutor related to an
            Appointment that is meant to be deleted, None
            otherwise.
        """
        if self.request.user != self.subscription.tutor.user:
            LOGGER.warning(
                "User %(username)s with ID %(id)s attempting to delete Appointment with ID %(appointment_id)s",
                {
                    "username": self.request.user.username,
                    "id": self.request.user.id,
                    "appointment_id": self.kwargs["pk"],
                },
            )
            return render(
                request=self.request,
                template_name="tutoringApp/forbidden.html",
                status=403,
                context={
                    "warning_message": "You are not allowed to delete the Appointment.",
                    "redirect_link": reverse("home:home"),
                    "redirect_destination": "home page",
                },
            )
