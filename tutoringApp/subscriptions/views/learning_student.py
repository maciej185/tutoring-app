"""Views for the `learning_student` page."""

from logging import getLogger
from typing import Any, Optional

from django.db.models import QuerySet
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.urls import reverse

from subscriptions.models import Subscription

LOGGER = getLogger(__name__)

from .learning import LearningView


class LearningStudentView(LearningView):
    """Display Lessons of a given Student.

    The view displays a list of Lesson objects are
    related to Appointment created for a given Subscription
    whose primary key has been passed as the URL parameter.
    """

    template_name = "subscriptions/learning/student.html"

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        """Ensure the user is the Student related to given Subscription."""
        user_not_student_warning_response = self._user_not_student_warning_response()
        return (
            user_not_student_warning_response
            if user_not_student_warning_response
            else super().get(request, *args, **kwargs)
        )

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        """Add data to the default context."""
        context = super().get_context_data(**kwargs)
        context["subscriptions"] = self._get_subscriptions()

        return context

    def _get_subscriptions(self) -> QuerySet[Subscription]:
        """Get all Subscriptions related to the current Student.

        Returns:
            A QuerySet with all Subscriptions objects
            related to the currently logged in Tutor.
        """
        return Subscription.objects.filter(student__user=self.request.user)

    def _user_not_student_warning_response(self) -> Optional[HttpResponse]:
        """Check if the currently logged in user is the Student related to the Subscription.

        Returns:
            An instance of the HttpResponse which renders a
            page with a warning message if the currently
            logged in user is not the Student related to the
            the Subscription object that is meant to be displayed.
        """
        if self.request.user != self.subscription.student.user:
            LOGGER.warning(
                "User %(username)s with ID %(id)s attempting to display learining page of Student with ID %(student_id)s.",
                {
                    "username": self.request.user.username,
                    "id": self.request.user.id,
                    "student_id": self.subscription.student.pk,
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
