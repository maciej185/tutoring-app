"""Views for displaying a single Lesson object."""
from abc import ABC, abstractmethod
from datetime import datetime, timezone
from typing import Any, Literal, Optional

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Model, Q
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.generic.detail import DetailView
from django.views.generic.edit import ProcessFormView

from lessons.forms import EntryForm, LessonStatusForm
from lessons.models import (
    Booking,
    Entry,
    Lesson,
    Material,
    Solution,
    Task,
    TaskStatusChoices,
)
from profiles.forms import AccountType


class DisplayLessonViewInterface(ABC):
    """Abstract base class for a view class for displaying a Lesson object."""

    @abstractmethod
    def _get_redirect_url(self) -> str:
        """Return an URL address that the user will be redirected to after submitting an entry."""


class DisplayLessonView(
    DetailView, ProcessFormView, LoginRequiredMixin, DisplayLessonViewInterface
):
    """Base view for displaying Lesson model instance."""

    model = Lesson

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        """Add Lesson-related objects to the context."""
        context = super().get_context_data(**kwargs)
        lesson = self.get_object()

        context["materials"] = Material.objects.filter(lesson=lesson)
        context["tasks"] = Task.objects.filter(lesson=lesson)
        context["entries"] = Entry.objects.filter(lesson=lesson)
        context["solutions"] = self._get_solutions()
        context["entry_form"] = EntryForm(initial={"lesson": self.kwargs["pk"]})

        return context

    def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        """Processing the data passed in EntryForm"""
        form = EntryForm(request.POST)
        if form.is_valid():
            entry = Entry(
                text=form.cleaned_data["text"],
                lesson=self.get_object(),
                from_student=request.session["account_type"]
                == AccountType.STUDENT.value,
            )
            entry.save()
        return HttpResponseRedirect(self._get_redirect_url())

    def _get_redirect_url() -> str:
        return reverse("home:home")

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

    def _get_redirect_url(self) -> str:
        """Redirect Student back to Lesson display page."""
        return reverse(
            "lessons:lesson_display_student", kwargs={"pk": self.kwargs["pk"]}
        )


class DisplayLessonTutorView(
    DisplayLessonView,
):
    """View for displaying Lesson objects from Tutor's perspective."""

    template_name = "lessons/display_4_tutor.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        """Include Tutor-specific content."""
        context = super().get_context_data(**kwargs)

        context["lesson_status_form"] = LessonStatusForm(
            data={"status": self.get_object().status}
        )

        context["lesson_pk"] = self.kwargs["pk"]

        context["lesson_happened"] = self.get_object().date < datetime.now(
            tz=timezone.utc
        )

        context["task_statuses"] = self._get_task_statuses()

        return context

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        """Ensure the user is the Tutor related to the lesson."""
        related_booking = self._get_related_booking()
        if related_booking:
            if request.user != related_booking.availability.service.tutor.user:
                return render(
                    request=self.request,
                    template_name="tutoringApp/forbidden.html",
                    status=403,
                    context={
                        "warning_message": "You are not allowed to view Lesson objects assigned to other Tutors.",
                        "redirect_link": reverse("home:home"),
                        "redirect_destination": "home page",
                    },
                )
        return super().get(request, *args, **kwargs)

    def _get_redirect_url(self) -> str:
        """Redirect Student back to Lesson display page."""
        return reverse("lessons:lesson_display_tutor", kwargs={"pk": self.kwargs["pk"]})

    def _get_task_statuses(self) -> list[Optional[Literal["approved", "rejected", ""]]]:
        """Return statuses of Tasks.

        Returns:
            A list with Task's statuses
            repesented as strings that will be used as class
            names in the template.
        """
        tasks = Task.objects.filter(lesson=self.get_object())
        statuses = []
        for task in tasks:
            if task.status == TaskStatusChoices.SOLUTION_APPROVED.value:
                statuses.append("approved")
            elif task.status == TaskStatusChoices.SOLUTION_DISMISSED.value:
                statuses.append("rejected")
            else:
                statuses.append("")
        return statuses
