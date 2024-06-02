"""Views for managing Subscriptions objects."""
from typing import Any, Optional

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models.query import QuerySet
from django.forms.models import BaseModelForm
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView

from profiles.forms import AccountType
from profiles.models import Profile
from subscriptions.forms import SubscriptionForm
from subscriptions.models import Subscription


class CreateSubscriptionView(CreateView, LoginRequiredMixin):
    """View for creating Subscription objects."""

    model = Subscription
    template_name = "subscriptions/create.html"
    form_class = SubscriptionForm

    def get_initial(self) -> dict[str, Any]:
        """Return initial Tutor data for the form."""
        return {"tutor": Profile.objects.get(user=self.request.user).pk}

    def get(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        """Check if current user is a Tutor."""
        user_is_not_tutor_response = self._user_is_not_tutor_response()
        return (
            user_is_not_tutor_response
            if user_is_not_tutor_response
            else super().get(request, *args, **kwargs)
        )

    def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        """Check if current user is a Tutor."""
        user_is_not_tutor_response = self._user_is_not_tutor_response()
        return (
            user_is_not_tutor_response
            if user_is_not_tutor_response
            else super().post(request, *args, **kwargs)
        )

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        subscription = Subscription(
            tutor=Profile.objects.get(user=self.request.user),
            student=form.cleaned_data["student"],
            subject=form.cleaned_data["subject"],
        )
        subscription.save()
        return HttpResponseRedirect(reverse("home:home"))

    def _user_is_not_tutor_response(self) -> Optional[HttpResponse]:
        """Check if current user is a Tutor.

        The method checks if the currently logged in user
        is a Tutor.

        Returns:
            An instance of the HttpResponse class which
            renders a warning page with redirection link
            if the currently logged in user is not a Tutor,
            None otherwise.
        """
        if Profile.objects.get(user=self.request.user).is_student():
            return render(
                request=self.request,
                template_name="tutoringApp/forbidden.html",
                status=403,
                context={
                    "warning_message": "Students are not allowed to create Subscriptions.",
                    "redirect_link": reverse("home:home"),
                    "redirect_destination": "home page",
                },
            )


class ListSubscriptionsStudentView(ListView, LoginRequiredMixin):
    """View for displaying subscriptions without details."""

    model = Subscription
    context_object_name = "subscriptions"
    template_name = "subscriptions/list/student.html"

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        """Redirect to a correct page in case a Tutor attempts to access the page."""
        if self.request.session["account_type"] == AccountType.TUTOR.value:
            return HttpResponseRedirect(reverse("subscriptions:learning_tutor_list"))
        return super().get(request, *args, **kwargs)

    def get_queryset(self) -> QuerySet[Any]:
        """Filter the fetched subscriptions for the current Student."""
        return Subscription.objects.filter(student__user=self.request.user)


class ListSubscriptionsTutorView(ListView, LoginRequiredMixin):
    """View for displaying subscriptions without details."""

    model = Subscription
    context_object_name = "subscriptions"
    template_name = "subscriptions/list/tutor.html"

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        """Redirect to a correct page in case a Student attempts to access the page."""
        if self.request.session["account_type"] == AccountType.STUDENT.value:
            return HttpResponseRedirect(reverse("subscriptions:learning_student_list"))
        return super().get(request, *args, **kwargs)

    def get_queryset(self) -> QuerySet[Any]:
        """Filter the fetched subscriptions for the current Student."""
        return Subscription.objects.filter(tutor__user=self.request.user)
