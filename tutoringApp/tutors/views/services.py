"""Views for configuring services offered by a Tutor."""
from logging import getLogger
from typing import Any, Optional, Union

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.generic.detail import DetailView
from django.views.generic.edit import ProcessFormView

from profiles.models import Profile
from tutors.forms import service_formset
from tutors.models import Service

LOGGER = getLogger(__name__)


class ServiceConfigurationView(DetailView, ProcessFormView, LoginRequiredMixin):
    model = Profile
    service_formset_errors = False
    service_formset_unique_error = False
    template_name = "tutors/services.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        """Add forms to the default context."""
        context = super().get_context_data(**kwargs)

        context["service_formset"] = service_formset(instance=self.get_object())

        context["service_formset_errors"] = self._check_for_service_formset_errors()

        context[
            "service_formset_unique_error"
        ] = self._check_for_service_formset_unique_error()

        context["currency"] = settings.CURRENCY

        return context

    def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        self._save_service_data()
        return HttpResponseRedirect(
            reverse("tutors:services", kwargs={"pk": self.kwargs["pk"]})
        )

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        """Check if the currently logged in user is configured as tutor in given Service object."""
        profile = Profile.objects.get(user=request.user)
        if profile != self.get_object():
            LOGGER.warning(
                "User %(username)s with id %(id)s attempting to configure services of %(service_tutor)s with id %(service_tutor_id)s!",
                {
                    "username": self.request.user.username,
                    "id": self.request.user.id,
                    "profile_owner": User.objects.get(pk=self.get_object().pk).username,
                    "profile_owner_id": self.get_object().pk,
                },
            )
            return render(
                request=request,
                template_name="tutoringApp/forbidden.html",
                status=403,
                context={
                    "warning_message": "You are not allowed to configure tutor's services!",
                    "redirect_link": reverse("home:home"),
                    "redirect_destination": "home page",
                },
            )

        return super().get(request, *args, **kwargs)

    def _save_service_data(self) -> Optional[HttpResponseRedirect]:
        """Save service data provided via formset.

        The method validates the formset and if there
        are no issues detected, the data gets saved
        and the user is taken to the next page whos
        URL is returned by self.get_success_url method.
        If any errors are spotted when validating the
        formset, the list of error messages gets
        added to session info and the value of
        'service_formset_errors' flag is set
        to True to mark that further error
        'handling' is needed.
        """
        filled_service_formset = service_formset(
            self.request.POST, instance=self.get_object()
        )
        if filled_service_formset.is_valid():
            try:
                instances = filled_service_formset.save()
            except IntegrityError:
                self.request.session[
                    "service_formset_unique_error"
                ] = "There are already default Services with 1 session defined."
                self.service_formset_unique_error = True
                return
            if instances:
                for instance in instances:
                    instance.is_default = False
                    instance.save()
                return
        self.request.session["service_formset_errors"] = filled_service_formset.errors
        self.service_formset_errors = True
        LOGGER.warning(
            "Serivce formset uploaded by %(username)s with id %(id)s contains errors: %(errors)s, %(non_form_errors)s"
            % {
                "username": self.request.user.username,
                "id": self.request.user.id,
                "errors": filled_service_formset.errors,
                "non_form_errors": filled_service_formset.non_form_errors(),
            }
        )

    def _check_for_service_formset_errors(self) -> Optional[list[dict[str, str]]]:
        """Check if error messages are present in session info.

        Returns:
            If error messages are present, the list containing
            them gets returned and the value is removed from the session.
            In other case, None is returned.
        """
        if self.request.session.get("service_formset_errors"):
            service_formset_errors = self.request.session.get("service_formset_errors")
            del self.request.session["service_formset_errors"]
            return service_formset_errors

    def _check_for_service_formset_unique_error(self) -> Optional[str]:
        """Check if errors about unique constraint violation are present in session info.

        Returns:
            Error message informing that the unique contrainst
            (only one Service with 1 as the value of `number_of_hours`)
            has been violated if form with such info has been submitted,
            None otherwise.
        """
        if self.request.session.get("service_formset_unique_error"):
            service_formset_unique_error = self.request.session.get(
                "service_formset_unique_error"
            )
            del self.request.session["service_formset_unique_error"]
            return service_formset_unique_error


@login_required
def service_delete_view(
    request: HttpRequest, service_id: int
) -> Union[HttpResponseRedirect, HttpResponse]:
    """Delete Service object with provided ID.

    The view first checks if the currently logged in user is
    the tutor related to a given Service. If not, the user
    is redicrected to a page with a warning message. In other
    case the Service object is deleted and the user is redirected
    back to service configuration page.

    Args:
        request: In instance of the HttpRequest class, containing
                every information about the request sent to the server.
        service_id: Primary key of the service object that is meant
                    to be deleted.

    Returns:
        An instance of HttpResponse class, redirecting the user
        back to service configuration page if the logged in user is
        the Service's `owner` or to a warning page otherwise.
    """
    service = Service.objects.get(pk=service_id)
    service_tutor_id = service.tutor.pk
    current_users_profile = Profile.objects.get(user=request.user)
    if current_users_profile != service.tutor:
        LOGGER.warning(
            "User %(username)s with id %(id)s attempting to delete services of %(service_tutor)s with id %(service_tutor_id)s!",
            {
                "username": request.user.username,
                "id": request.user.id,
                "service_tutor": User.objects.get(pk=service_tutor_id).username,
                "service_tutor_id": service_tutor_id,
            },
        )
        return render(
            request=request,
            template_name="tutoringApp/forbidden.html",
            status=403,
            context={
                "warning_message": "You are not allowed to delete tutor's services!",
                "redirect_link": reverse("home:home"),
                "redirect_destination": "home page",
            },
        )
    service.delete()
    LOGGER.debug(
        "Service with id %(service_id)s successfuly deleted.",
        {
            "service_id": service_id,
        },
    )
    return HttpResponseRedirect(
        reverse("tutors:services", kwargs={"pk": service_tutor_id})
    )
