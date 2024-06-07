"""Views for chat-related functionalities."""
from typing import Any

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.generic.list import ListView

from profiles.forms import AccountType
from profiles.models import Profile
from subscriptions.models import Subscription


class StudentChatView(ListView, LoginRequiredMixin):
    """View for displaying available chat partners for Students."""

    model = Profile
    template_name = "chat\chat_student.html"
    context_object_name = "profiles"

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        """Check if the current user is the intented Student.

        The method checks if the currently logged in user is the Student
        whos PK has been passed as the URL argument.

        Return:
            An instance of the HttpResponse class rendering an
            appropriate redirection page if the current user
            is not the intented Student, otherwise a page with a
            list of Tutors that the user is 'subscribed' to.
        """
        if (
            self.request.session["account_type"] == AccountType.TUTOR.value
            or self.request.user.pk != self.kwargs["student_id"]
        ):
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
        return super().get(request, *args, **kwargs)

    def get_queryset(self) -> list[Profile]:
        """Fetch a list of Tutors that the given Student is 'subscribed' to."""
        return list(
            set(
                [
                    subscription.tutor
                    for subscription in Subscription.objects.filter(
                        student__pk=self.kwargs["student_id"]
                    )
                ]
            )
        )


class TutorChatView(ListView, LoginRequiredMixin):
    """View for displaying available chat partners for Tutors."""

    model = Profile
    template_name = "chat\chat_tutor.html"
    context_object_name = "profiles"

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        """Check if the current user is the intented Tutor.

        The method checks if the currently logged in user is the Tutor
        whos PK has been passed as the URL argument.

        Return:
            An instance of the HttpResponse class rendering an
            appropriate redirection page if the current user
            is not the intented Tutor, otherwise a page with a
            list of Students that are 'subscribed' to the given Tutor.
        """
        if (
            self.request.session["account_type"] == AccountType.STUDENT.value
            or self.request.user.pk != self.kwargs["tutor_id"]
        ):
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
        return super().get(request, *args, **kwargs)

    def get_queryset(self) -> list[Profile]:
        """Fetch a list of Students that are 'subscribed' to the given Tutor."""
        return list(
            set(
                [
                    subscription.student
                    for subscription in Subscription.objects.filter(
                        tutor__pk=self.kwargs["tutor_id"]
                    )
                ]
            )
        )


class StudentChatWindowView(StudentChatView):
    """View for displaying available chat partners for Students and the chat window."""

    template_name = "chat\chat_student_window.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        """Add name of the receiving Tutor to the context."""
        context = super().get_context_data(**kwargs)
        context["tutor"] = Profile.objects.get(pk=self.kwargs["tutor_id"])
        return context

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        """Check if the given user is the intented Student or Tutor."""
        if self.request.user.pk != self.kwargs["student_id"]:
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
        return super().get(request, *args, **kwargs)


class TutorChatWindowView(TutorChatView):
    """View for displaying available chat partners for Tutors and the chat window."""

    template_name = "chat\chat_tutor_window.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        """Add name of the receiving Student to the context."""
        context = super().get_context_data(**kwargs)
        context["student"] = Profile.objects.get(pk=self.kwargs["student_id"])
        return context

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        """Check if the given user is the intented Student or Tutor."""
        if self.request.user.pk != self.kwargs["tutor_id"]:
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
        return super().get(request, *args, **kwargs)
