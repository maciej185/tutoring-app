from logging import getLogger
from typing import Optional, Union

from django.forms.models import BaseModelForm
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse_lazy

from profiles.forms import profile_language_list_formset, subject_formset

from .profile import UpdateProfileView

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
        self._save_subject_data()
        self._save_profile_language_data()
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

        context[
            "profile_language_formset_errors"
        ] = self._check_for_profile_language_formset_error()
        context["subject_formset_errors"] = self._check_for_subject_formset_error()

        return context

    def _save_subject_data(self) -> None:
        """Save subject data provided via formset.

        The method validates the formset and if there
        are no issues detected, the data gets saved
        and the user is taken to the next page whos
        URL is returned by self.get_success_url method.
        If any errors are spotted when validating the
        formset, the list of error messages gets
        added to session info and the value of
        'subject_formset_errors' flag is set
        to True to mark that further error
        'handling' is needed.
        """
        filled_subject_formset = subject_formset(
            self.request.POST, instance=self.get_object()
        )
        if filled_subject_formset.is_valid():
            filled_subject_formset.save()
        else:
            self.request.session[
                "subject_formset_errors"
            ] = filled_subject_formset.errors
            self.subject_formset_errors = True
            LOGGER.warning(
                "Subject formset uploaded by %(username)s with id %(id)s contains errors: %(errors)s"
                % {
                    "username": self.request.user.username,
                    "id": self.request.user.id,
                    "errors": filled_subject_formset.errors,
                }
            )

    def _save_profile_language_data(self):
        """Save language data provided via formset.

        The method validates the formset and if there
        are no issues detected, the data gets saved
        and the user is taken to the next page whos
        URL is returned by self.get_success_url method.
        If any errors are spotted when validating the
        formset, the list of error messages gets
        added to session info and the value of
        'profile_language_formset_errors' flag is set
        to True to mark that further error
        'handling' is needed.
        """
        filled_profile_language_formset = profile_language_list_formset(
            self.request.POST, instance=self.get_object()
        )
        if filled_profile_language_formset.is_valid():
            filled_profile_language_formset.save()
        else:
            self.request.session[
                "profile_language_formset_errors"
            ] = filled_profile_language_formset.errors
            self.profile_language_formset_errors = True
            LOGGER.warning(
                "Languages formset uploaded by %(username)s with id %(id)s contains errors: %(errors)s"
                % {
                    "username": self.request.user.username,
                    "id": self.request.user.id,
                    "errors": filled_profile_language_formset.errors,
                }
            )

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

    def _check_for_subject_formset_error(self) -> Optional[list[dict[str, str]]]:
        """Check if error messages are present in session info.

        Returns:
            If error messages are present, the list containing
            them gets returned and the value is removed from the session.
            In other case, None is returned.
        """
        if self.request.session.get("subject_formset_errors"):
            subject_formset_errors = self.request.session.get("subject_formset_errors")
            del self.request.session["subject_formset_errors"]
            return subject_formset_errors

    def _check_for_profile_language_formset_error(
        self,
    ) -> Optional[list[dict[str, str]]]:
        """Check if error messages are present in session info.

        Returns:
            If error messages are present, the list containing
            them gets returned and the value is removed from the session.
            In other case, None is returned.
        """
        if self.request.session.get("profile_language_formset_errors"):
            profile_language_formset_errors = self.request.session.get(
                "profile_language_formset_errors"
            )
            del self.request.session["profile_language_formset_errors"]
            return profile_language_formset_errors
