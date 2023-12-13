from logging import getLogger
from typing import Any, Literal, Optional, Union

from django.conf import settings
from django.forms.models import BaseInlineFormSet, BaseModelForm
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.urls import reverse_lazy

from profiles.forms import profile_language_list_formset, subject_formset
from profiles.models import ProfileLanguageList
from tutors.models import Service

from .update import UpdateProfileView

LOGGER = getLogger(__name__)


class UpdateTutorProfileView(UpdateProfileView):
    template_name = "profiles/update_tutor.html"
    subject_formset_errors = False
    profile_language_formset_errors = False

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
        self._save_education_data()
        self._save_formset_data(
            profile_language_list_formset, "profile_language_formset_errors"
        )
        self._save_formset_data(subject_formset, "subject_formset_errors")
        self._save_user_data()

        if not self._additional_forms_have_errors():
            LOGGER.debug(
                "Profile of user %(username)s with id %(id)s successfuly updated.",
                {"username": self.request.user.username, "id": self.request.user.id},
            )
            return super().form_valid(form)
        return HttpResponseRedirect(
            reverse_lazy("profiles:tutor_update", kwargs={"pk": self.kwargs["pk"]})
        )

    def get_context_data(self, **kwargs):
        """Add formsets and other necessary info to default context."""
        context = super().get_context_data(**kwargs)

        context["subject_formset"] = subject_formset(instance=self.get_object())
        context["profile_language_list_formset"] = profile_language_list_formset(
            instance=self.get_object()
        )

        context["profile_language_formset_errors"] = self._check_for_formset_error(
            "profile_language_formset_errors"
        )
        context["subject_formset_errors"] = self._check_for_formset_error(
            "subject_formset_errors"
        )

        context["currency"] = settings.CURRENCY

        context["subject_objects_in_db"] = len(
            Service.objects.filter(tutor=self.get_object())
        )
        context["profile_language_list_objects_in_db"] = len(
            ProfileLanguageList.objects.filter(profile=self.get_object())
        )

        return context

    def _additional_forms_have_errors(self) -> bool:
        """Check if any of the additional forms have errors.

        The method extends the results of the implementation
        in the base class (UpdateProfileView) by also checking
        for errors in formsets specific to updating Tutor's profile.

        Returns:
            Boolean info indicating any errors
            with additional forms added manually to the
            context.
        """
        error_info = super()._additional_forms_have_errors()
        return any(
            [
                error_info,
                self.subject_formset_errors,
                self.profile_language_formset_errors,
            ]
        )

    def get(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        """Ensure correct update page is displayed according to Profile's type."""
        requested_profile = self.model.objects.get(pk=self.kwargs["pk"])
        if requested_profile.is_student():
            return HttpResponseRedirect(
                reverse_lazy(
                    "profiles:student_update", kwargs={"pk": self.kwargs["pk"]}
                )
            )
        return super().get(request, *args, **kwargs)

    def _save_formset_data(
        self,
        formset_class: type[BaseInlineFormSet],
        error_session_key: Literal[
            "profile_language_formset_errors", "subject_formset_errors"
        ],
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

            if error_session_key == "profile_language_formset_errors":
                self.profile_language_formset_errors = True
            elif error_session_key == "subject_formset_errors":
                self.subject_formset_errors = True

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
        error_session_key: Literal[
            "profile_language_formset_errors", "subject_formset_errors"
        ],
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
