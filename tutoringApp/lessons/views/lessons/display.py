"""Views for displaying a single Lesson object."""
from typing import Any, Optional

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Model, Q
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.generic.detail import DetailView
from django.views.generic.edit import FormMixin

from lessons.forms import EntryForm
from lessons.models import Booking, Entry, Lesson, Material, Solution, Task


class DisplayLessonView(DetailView, FormMixin, LoginRequiredMixin):
    """Base view for displaying Lesson model instance."""

    model = Lesson
    form_class = EntryForm

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        """Add Lesson-related objects to the context."""
        context = super().get_context_data(**kwargs)
        lesson = self.get_object()

        context["materials"] = Material.objects.filter(lesson=lesson)
        context["tasks"] = Task.objects.filter(lesson=lesson)
        context["entries"] = Entry.objects.filter(lesson=lesson)
        context["solutions"] = self._get_solutions()

        return context

    def get_initial(self) -> dict[str, Any]:
        """Return initial data for the form."""
        return {"lesson": self.kwargs["pk"]}

    def _get_related_booking(self) -> Optional[Booking]:
        """Fetch a related Booking object if it exists.

        Returns:
            Instance of the Booking model related to the
            currently updated Lesson model instance if such
            Booking exists (Lessons can also be linked to Appointment
            objects), None otherwise.
        """
        try:
            return Booking.objects.get(lesson_info=self.get_object())
        except Booking.DoesNotExist:
            return

    def _get_solutions(self) -> list[Optional[Solution]]:
        """Fetch Solutions for Tasks related to displayed Lesson.

        Returns:
            A list with the same length as the length
            returned by filtering Task object to get only
            the ones related to displayed Lesson. If no
            solution has been uploaded to a Task, there
            will be None inserted in the corresponsing solution
            in the list.
        """
        return [
            self._get_object_no_exception(Solution, Q(task=task))
            for task in Task.objects.filter(lesson=self.get_object())
        ]

    @staticmethod
    def _get_object_no_exception(model: type[Model], query: Q) -> Optional[Model]:
        """Get model instance using provided query expression.

        Args:
            model: Class inheriting from Model on which
                    the query will be executed.
            query: An instance of the Q class, representing
                    an SQL query expression to fetch
                    the desired model instance.
        Returns:
            Instance of the given model fetched using the
            provided query if it exists, None otherwise.
        """
        try:
            return model.objects.get(query)
        except model.DoesNotExist:
            return


class DisplayLessonStudentView(
    DisplayLessonView,
):
    """View for displaying Lesson objects from Studnet's perspective."""

    template_name = "lessons/display_4_student.html"

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        """Ensure the user is the Student related to the lesson."""
        related_booking = self._get_related_booking()
        if related_booking:
            if request.user != related_booking.student.user:
                return render(
                    request=self.request,
                    template_name="tutoringApp/forbidden.html",
                    status=403,
                    context={
                        "warning_message": "You are not allowed to view Lesson objects assigned to other Students.",
                        "redirect_link": reverse("home:home"),
                        "redirect_destination": "home page",
                    },
                )
        return super().get(request, *args, **kwargs)
