"""Views for creating and managing profile objects."""
from typing import Optional, Union

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.forms.models import BaseModelForm
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic.edit import UpdateView

from profiles.forms import (
    AccountType,
    StudentProfileForm,
    UpdateUserForm,
    education_formset,
)
from profiles.models import Education, Profile


@login_required
def create_profile_view(request: HttpRequest, user_id: int) -> HttpResponseRedirect:
    """Create the Profile object and redirect the user.

    The view creates the Profile object based on the
    provided User PK and then redirects the user to the page
    where additional profile information can be filled in.
    """
    user = get_object_or_404(User, pk=user_id)
    profile = Profile(user=user)
    profile.save()
    request.session["profile_setup"] = True
    request.session["profile_pic_url"] = profile.profile_pic.url
    return HttpResponseRedirect(reverse("profiles:update", kwargs={"pk": user_id}))


class UpdateProfileView(UpdateView, LoginRequiredMixin):
    """View for updating the profile's information."""

    model = Profile
    education_formset_errors = False
    user_form_errros = False

    def get_context_data(self, **kwargs):
        """Add formsets and other necessary info to default context."""
        context = super().get_context_data(**kwargs)

        context["education_formset_errors"] = self._check_for_education_formset_error()

        context["education_formset"] = education_formset(instance=self.get_object())

        context["profile_setup"] = bool(self.request.session.get("profile_setup"))
        self._remove_info_about_profile_setup_from_sessions()

        context["user_form"] = self._get_bound_user_update_form()

        context["is_student"] = self._check_if_user_is_student()

        return context

    def get_form_class(self) -> type[BaseModelForm]:
        """Return profile Form corresponding to the account type."""
        return StudentProfileForm if self._check_if_user_is_student() else None

    def get_success_url(self) -> str:
        """Redirect the user back to their profile."""
        self._update_profile_pic_url()
        return reverse("home:home")

    def get_template_names(self) -> list[str]:
        return (
            ["profiles/update_student.html"]
            if self._check_if_user_is_student()
            else ["profiles/update_tutor.html"]
        )

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
        self._save_user_data()

        if not self._additional_forms_have_errors():
            return super().form_valid(form)
        return HttpResponseRedirect(
            reverse_lazy("profiles:update", kwargs={"pk": self.kwargs["pk"]})
        )

    def _save_education_data(self) -> Optional[HttpResponseRedirect]:
        """Save education data provided via formset.

        The method validates the formset and if there
        are no issues detected, the data gets saved
        and the user is taken to the next page whos
        URL is returned by self.get_success_url method.
        If any errors are spotted when validating the
        formset, the list of error messages gets
        added to session info and the value of
        'education_formset_errors' flag is set
        to True to mark that further error
        'handling' is needed.
        """
        filled_education_formset = education_formset(
            self.request.POST, instance=self.get_object()
        )
        if filled_education_formset.is_valid():
            filled_education_formset.save()
        else:
            self.request.session[
                "education_formset_errors"
            ] = filled_education_formset.errors
            self.education_formset_errors = True

    def _save_user_data(self) -> None:
        """Save User's updated data.

        The method instanciates the UpdateUserForm
        with the data provided by the user via request and
        the current information stored in the instance of
        the User model refererring to the Profile that is
        currently being updated.
        """
        user = User.objects.get(pk=self.kwargs["pk"])
        update_user_form = UpdateUserForm(self.request.POST, instance=user)
        if update_user_form.is_valid():
            update_user_form.save()
        else:
            self.request.session["user_form_errors"] = update_user_form.errors
            self.user_form_errros = True

    def _remove_info_about_profile_setup_from_sessions(self) -> None:
        """Remove info about whether profile is being set up from session.

        The method attempts to remove the 'profile_setup' key from
        the session object after it has been passed to the context.
        """
        try:
            del self.request.session["profile_setup"]
        except KeyError:
            return

    def _check_if_user_is_student(self) -> bool:
        """Checks is the currently logged in user is a Student.

        The method uses the value of the 'account_type' key in the
        self.request.session object to determine whether the user is
        a Student or not.

        Return:
            Boolean info about whether the user is a Student.
        """
        return (
            True
            if self.request.session["account_type"] == AccountType.STUDENT.value
            else False
        )

    def _get_bound_user_update_form(self) -> UpdateUserForm:
        """Return a form for updating User object's info.

        Returns:
            A form for modifying the User object corresponsing
            to the given profile with initial info being populated.
        """
        user = User.objects.get(pk=self.kwargs["pk"])
        return UpdateUserForm(instance=user)

    def _check_for_education_formset_error(self) -> Optional[list[dict[str, str]]]:
        """Check if error messages are present in session info.

        Returns:
            If error messages are present, the list containing
            them gets returned and the value is removed from the session.
            In other case, None is returned.
        """
        if self.request.session.get("education_formset_errors"):
            education_formset_errors = self.request.session.get(
                "education_formset_errors"
            )
            del self.request.session["education_formset_errors"]
            return education_formset_errors

    def _check_for_user_form_error(self) -> Optional[list[dict[str, str]]]:
        """Check if error messages are present in session info.

        Returns:
            If error messages are present, the dictionary containing
            them gets returned and the value is removed from the session.
            In other case, None is returned.
        """
        if self.request.session.get("user_form_errors"):
            education_formset_errors = self.request.session.get("user_form_errors")
            del self.request.session["user_form_errors"]
            return education_formset_errors

    def _additional_forms_have_errors(self) -> bool:
        """Check if any of the additional forms have errors.

        The method uses the values of the class's attributes
        that indicate formset and form errors.

        Returns:
            Boolean info indicating any errors
            with additional forms added manually to the
            context.
        """
        return any([self.education_formset_errors, self.user_form_errros])

    def _update_profile_pic_url(self) -> None:
        """Update current user's profile picture URL in session.

        After the profile (potentially including profile picture)
        has been successfully updated, the current profile picture
        URL stored in the session info needs updating as well.
        """
        self.request.session["profile_pic_url"] = self.get_object().profile_pic.url


@login_required
def delete_education_object_view(_request, pk: int) -> HttpResponseRedirect:
    """Delete Education object and redirect back to profile update page.

    The method deletes the instance of the Education model who's
    PK has been passed in the URL. The user is then redirected back
    to profile update page.

    Args:
        request: An instance of the HttpRequest class, representing
                the actual HTTP request being sent to the server.
        pk: PK of the Education object that is meant to
                        be deleted.
    Returns:
        An instance of the HttpResponseRedirect class, redirecting the
        user back to the profile update page.
    """
    education = get_object_or_404(Education, pk=pk)
    profile = education.profile
    education.delete()
    return HttpResponseRedirect(reverse("profiles:update", kwargs={"pk": profile.pk}))
