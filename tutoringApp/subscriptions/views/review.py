"""Module containing reviews-related views."""

from typing import Any, Optional

from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import BaseModelForm
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views.generic.edit import CreateView, DeleteView

from subscriptions.forms import ReviewForm
from subscriptions.models import Review, Subscription


class CreateReviewView(CreateView, LoginRequiredMixin):
    """View for creating reviews."""

    model = Review
    template_name = "subscriptions/review/create.html"
    form_class = ReviewForm

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["subscription"] = Subscription.objects.get(pk=self.kwargs["subscription_id"])
        return context

    def get_initial(self) -> dict[str, Any]:
        """Return initial Subscription data for the form."""
        return {"subscription": self.kwargs["subscription_id"]}

    def get(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        """Check if the currently logged in user is a Student related to the given Subscription."""
        user_is_not_correct_student_tutor_response = self._user_is_not_correct_student_response()
        return (
            user_is_not_correct_student_tutor_response
            if user_is_not_correct_student_tutor_response
            else super().get(request, *args, **kwargs)
        )

    def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        """Check if the currently logged in user is a Student related to the given Subscription."""
        user_is_not_correct_student_tutor_response = self._user_is_not_correct_student_response()
        return (
            user_is_not_correct_student_tutor_response
            if user_is_not_correct_student_tutor_response
            else super().post(request, *args, **kwargs)
        )

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        """Create the instance of the Review model and redirect the User back to the subscription page."""
        review = Review(
            subscription=Subscription.objects.get(pk=self.kwargs["subscription_id"]),
            star_rating=form.cleaned_data["star_rating"],
            text=form.cleaned_data["text"],
        )
        review.save()
        return HttpResponseRedirect(
            reverse(
                "subscriptions:learning_student",
                kwargs={"subscription_id": self.kwargs["subscription_id"]},
            )
        )

    def _user_is_not_correct_student_response(self) -> Optional[HttpResponse]:
        """Check if the current user is the Student related to the given Subcription.

        Reviews can only be made by Students who are related to the given
        Subscription. The method checks if the current user is that Student
        and if not, a warnign page with redirection link is rendered.

        Returns:
            An instance of the HttpResponse class which
            renders a warning page with redirection link
            if the currently logged in user is not a correct Student,
            None otherwise.
        """
        subscription = Subscription.objects.get(pk=self.kwargs["subscription_id"])
        if self.request.user.pk != subscription.student.pk:
            return render(
                request=self.request,
                template_name="tutoringApp/forbidden.html",
                status=403,
                context={
                    "warning_message": "You are not allowed to create a Review for that Subscription.",
                    "redirect_link": reverse("home:home"),
                    "redirect_destination": "home page",
                },
            )


class DeleteReviewView(DeleteView, LoginRequiredMixin):
    """View for deleting reviews."""

    success_url = reverse_lazy
    model = Review
    pk_url_kwarg = "review_id"
    template_name = "subscriptions/review/delete.html"

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        """Check if the currently logged in user is a Student and an author of the given Review."""
        user_is_not_correct_student_response = self._user_is_not_correct_student_response()
        return (
            user_is_not_correct_student_response
            if user_is_not_correct_student_response
            else super().get(request, *args, **kwargs)
        )

    def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        user_is_not_correct_student_response = self._user_is_not_correct_student_response()
        return (
            user_is_not_correct_student_response
            if user_is_not_correct_student_response
            else super().post(request, *args, **kwargs)
        )

    def _user_is_not_correct_student_response(self) -> Optional[HttpResponse]:
        """Check if the current user is the Student related to the given Subcription.

        Reviews can only be made by Students who are related to the given
        Subscription. The method checks if the current user is that Student
        and if not, a warnign page with redirection link is rendered.

        Returns:
            An instance of the HttpResponse class which
            renders a warning page with redirection link
            if the currently logged in user is not a correct Student,
            None otherwise.
        """
        subscription = self.get_object().subscription
        if self.request.user.pk != subscription.student.pk:
            return render(
                request=self.request,
                template_name="tutoringApp/forbidden.html",
                status=403,
                context={
                    "warning_message": "You are not allowed to delete the Review!",
                    "redirect_link": reverse("home:home"),
                    "redirect_destination": "home page",
                },
            )

    def get_success_url(self) -> str:
        """Redirect the user back to the Subscription page."""
        return reverse_lazy(
            "subscriptions:learning_student",
            kwargs={"subscription_id": self.get_object().subscription.pk},
        )
