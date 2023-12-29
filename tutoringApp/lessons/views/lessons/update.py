"""Views for updating a single Lesson object."""
from logging import getLogger
from typing import Any, Literal, Optional, Union

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import BaseInlineFormSet, BaseModelForm
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views.generic.edit import UpdateView

from lessons.forms import LessonForm, material_formset, task_formset
from lessons.models import Booking, Lesson, Material, Task
from profiles.models import Profile
from tutors.models import Service

LOGGER = getLogger(__name__)


class UpdateLessonView(UpdateView, LoginRequiredMixin):
    """View for updating a single Lesson object."""

    task_formset_errors = False
    material_formset_errors = False

    model = Lesson
    form_class = LessonForm
    template_name = "lessons/update.html"

    def get_success_url(self) -> str:
        """Redirect the Tutor back to their Bookings."""
        return reverse_lazy("lessons:booking_display_tutor")

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        """Include additional formsets and information in the default context."""
        context = super().get_context_data(**kwargs)

        context["task_formset"] = task_formset(instance=self.get_object())
        context["material_formset"] = material_formset(instance=self.get_object())

        context["task_formset_errors"] = self._check_for_formset_error(
            "task_formset_errors"
        )
        context["material_formset_errors"] = self._check_for_formset_error(
            "material_formset_errors"
        )

        context["related_booking"] = self._get_related_booking()

        context["material_objects_in_db"] = len(
            Material.objects.filter(lesson=self.get_object())
        )

        context["task_objects_in_db"] = len(
            Task.objects.filter(lesson=self.get_object())
        )

        return context

    def form_valid(
        self, form: BaseModelForm
    ) -> Union[HttpResponse, HttpResponseRedirect]:
        """Check valididty of the main form and additional formsets.

        The method checks if the main form and
        any other form rendered on the page is valid.
        If so, the user gets redirected further to the page
        whos URL is returned by the self.get_success_url method.
        In any other case the user is redirected back to the
        profile update page and the error messages are getting
        displayed.

        Args:
            form: An instance of the form class
                    (the class is specified in the
                    self.get_form_class method)
                    with data provided by the user.
        Returns:
            HttpResponse if all forms are valid, HttpResponseRedirect
            otherwise.
        """
        self._save_formset_data(task_formset, "task_formset_errors")
        self._save_formset_data(material_formset, "material_formset_errors")
        if not self._additional_forms_have_errors():
            LOGGER.debug(
                "Lesson assigned to %(username)s with id %(id)s successfuly updated.",
                {"username": self.request.user.username, "id": self.request.user.id},
            )
            return super().form_valid(form)
        return HttpResponseRedirect(
            reverse_lazy("lessons:lesson_update", kwargs={"pk": self.kwargs["pk"]})
        )

    def get(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        """Ensure that current user is the Tutor assigned to the Lesson."""
        related_booking = self._get_related_booking()
        if related_booking:
            tutor = related_booking.availability.service.tutor.user
            if request.user != tutor:
                return render(
                    request=self.request,
                    template_name="tutoringApp/forbidden.html",
                    status=403,
                    context={
                        "warning_message": "You are not allowed to update Lesson object assigned to the Tutor.",
                        "redirect_link": reverse("home:home"),
                        "redirect_destination": "home page",
                    },
                )
        return super().get(request, *args, **kwargs)

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

    def _save_formset_data(
        self,
        formset_class: type[BaseInlineFormSet],
        error_session_key: Literal["task_formset_errors", "material_formset_errors"],
    ) -> None:
        """Save data provided via formset.

        The method validates the formset and if there
        are no issues detected, the data gets saved
        and the user is taken to the next page whos
        URL is returned by self.get_success_url method.
        If any errors are spotted when validating the
        formset, the list of error messages gets
        added to session info and the value of
        an appropriate flag is set to True to mark that
        further error 'handling' is needed.

        Args:
            formset_class: An instance of the formset
                            that the data was originally
                            send in.
            error_session_key: The key that the error list
                                will be assigned to in the
                                session object. The value of this
                                argument will also allow to
                                decide which flag (class's attribute)
                                will be set to True in case of errors.
        """
        filled_formset = formset_class(self.request.POST, instance=self.get_object())
        if filled_formset.is_valid():
            filled_formset.save()
        else:
            self.request.session[error_session_key] = filled_formset.errors

            if error_session_key == "task_formset_errors":
                self.task_formset_errors = True
            elif error_session_key == "material_formset_errors":
                self.material_formset_errors = True

            LOGGER.warning(
                "%(formset)s uploaded by %(username)s with id %(id)s contains errors: %(errors)s"
                % {
                    "formset": formset_class.__name__,
                    "username": self.request.user.username,
                    "id": self.request.user.id,
                    "errors": filled_formset.errors,
                }
            )

    def _check_for_formset_error(
        self,
        error_session_key: Literal["task_formset_errors", "material_formset_errors"],
    ) -> Optional[list[dict[str, str]]]:
        """Check if error messages are present in session info.

        Args:
            error_session_key: Key with the error name to be
                                searched for in the session
                                object.

        Returns:
            If error messages are present, the list containing
            them gets returned and the value is removed from the session.
            In other case, None is returned.
        """
        if self.request.session.get(error_session_key):
            formset_errors = self.request.session.get(error_session_key)
            del self.request.session[error_session_key]
            return formset_errors

    def _additional_forms_have_errors(self) -> bool:
        """Check if any of the additional forms have errors.

        The method uses the values of the class's attributes
        that indicate formset and form errors.

        Returns:
            Boolean info indicating any errors
            with additional forms added manually to the
            context.
        """
        return any([self.task_formset_errors, self.material_formset_errors])


def user_is_not_tutor(request: HttpRequest, tutor: Profile) -> Optional[HttpResponse]:
    """Ensure that currently logged in user is the provided Tutor.

    Args:
        request: An instance of the HttpRequest class, containing
                every information about the request sent to the server.
        tutor: Instance of the Profile model, representing assigned to
                a given object that the is meaning to modify/delete.
    Returns:
        Instance of the HttpResponse class rendering a page with warning
        message and a redirection link if the currently logged in user is
        not the specified Tutor, None otherwise.
    """
    if request.user != tutor.user:
        return render(
            request=request,
            template_name="tutoringApp/forbidden.html",
            status=403,
            context={
                "warning_message": "You are not allowed to modfify the object.",
                "redirect_link": reverse("home:home"),
                "redirect_destination": "home page",
            },
        )


@login_required
def delete_task_view(request: HttpRequest, task_id: int) -> HttpResponse:
    """View for deleting a single Task object.

    Args:
        request: An instance of the HttpRequest class, containing
                every information about the request sent to the server.
        task_id: Primary key of the Task object that is meant to be deleted.

    Returns:
        Instance of the HttpResponse class, redirecting the user either to
        a warning page if they are not the Tutor related to a given Task
        or to a page where the related Lesson can be updated.
    """
    task = Task.objects.get(pk=task_id)
    service = Service.objects.get(availability__booking__lesson_info__task=task)
    lesson = Lesson.objects.get(task=task)
    user_is_not_tutor_res = user_is_not_tutor(request, service.tutor)
    if user_is_not_tutor_res:
        return user_is_not_tutor_res
    task.delete()
    return HttpResponseRedirect(
        reverse("lessons:lesson_update", kwargs={"pk": lesson.pk})
    )


@login_required
def delete_material_view(request: HttpRequest, material_id: int) -> HttpResponse:
    """View for deleting a single Material object.

    Args:
        request: An instance of the HttpRequest class, containing
                every information about the request sent to the server.
        task_id: Primary key of the Material object that is meant to be deleted.

    Returns:
        Instance of the HttpResponse class, redirecting the user either to
        a warning page if they are not the Tutor related to a given Material
        or to a page where the related Lesson can be updated.
    """
    material = Material.objects.get(pk=material_id)
    service = Service.objects.get(availability__booking__lesson_info__material=material)
    lesson = Lesson.objects.get(material=material)
    user_is_not_tutor_res = user_is_not_tutor(request, service.tutor)
    if user_is_not_tutor_res:
        return user_is_not_tutor_res
    material.delete()
    return HttpResponseRedirect(
        reverse("lessons:lesson_update", kwargs={"pk": lesson.pk})
    )
