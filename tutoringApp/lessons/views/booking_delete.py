"""Views for deleting Booking objects."""
from typing import Any, Optional

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views.generic.edit import DeleteView

from lessons.models import Booking
from profiles.models import Profile


class BookingDeleteView(DeleteView, LoginRequiredMixin):
    """View for deleting Booking objects."""

    template_name = "booking/delete.html"
    model = Booking
    success_url = reverse_lazy("lessons:booking_display_student")

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        """Ensure the requestor is the Student related to the Booking object."""
        for check_function in [
            self._requestor_not_related_student_response,
            self._related_availability_is_oudated,
        ]:
            check_result = check_function()
            if check_result:
                return check_result
        return super().get(request, *args, **kwargs)

    def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        """Ensure the requestor is the Student related to the Booking object."""
        for check_function in [
            self._requestor_not_related_student_response,
            self._related_availability_is_oudated,
        ]:
            check_result = check_function()
            if check_result:
                return check_result
        return super().post(request, *args, **kwargs)

    def _requestor_not_related_student_response(self) -> Optional[HttpResponse]:
        """Check if the currently logged in user is the Student related to the Booking object.

        Returns:
            An instance of the HttpResponse class rendering a page with
            warning message and redirection link jf the currently logged
            in user is not the Student related to the Booking object that
            is meant to be deleted, None otherwise.
        """
        if self.get_object().student != Profile.objects.get(user=self.request.user):
            return render(
                request=self.request,
                template_name="tutoringApp/forbidden.html",
                status=403,
                context={
                    "warning_message": "You are not allowe to delete another Student's Booking.",
                    "redirect_link": reverse("home:home"),
                    "redirect_destination": "home page",
                },
            )

    def _related_availability_is_oudated(self) -> Optional[HttpResponse]:
        """Check if the related Availability is not outdated.

        Returns:
            An instance of the HttpResponse class redndering a page with
            warning message and redirection link if the Availavility
            object related to the Booking that is meant to be deleted is
            outdated, None otherwise.
        """
        if self.get_object().availability.is_outdated:
            return render(
                request=self.request,
                template_name="tutoringApp/forbidden.html",
                status=403,
                context={
                    "warning_message": "The Availability object related to the current Booking is outdated.",
                    "redirect_link": reverse("lessons:booking_display_student"),
                    "redirect_destination": "your Bookings.",
                },
            )
