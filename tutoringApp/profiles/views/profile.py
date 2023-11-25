"""Views for creating and managing profile objects."""
from logging import getLogger
from typing import Any, Optional

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse, reverse_lazy
from django.views.generic.edit import UpdateView

from profiles.forms import AccountType, ProfileForm, UpdateUserForm, education_formset
from profiles.models import Education, Profile

LOGGER = getLogger(__name__)


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
    LOGGER.debug(
        "Profile for %(username)s with id %(id)s created."
        % {"username": user.username, "id": user.pk}
    )
    request.session["profile_setup"] = True
    request.session["profile_pic_url"] = profile.profile_pic.url
    return HttpResponseRedirect(reverse("profiles:update", kwargs={"pk": user_id}))


class UpdateProfileView(UpdateView, LoginRequiredMixin):
    """View for updating the profile's information."""

    model = Profile
    form_class = ProfileForm
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

        return context

    def get_success_url(self) -> str:
        """Redirect the user back to their profile."""
        self._update_profile_pic_url()
        return reverse("home:home")

    def get(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        """Additional checks to make sure the current user is the profile's owner."""
        if request.user != self.get_object().user:
            LOGGER.warning(
                "User %(username)s with id %(id)s attempting to edit profile of %(profile_owner)s with id %(profile_owner_id)s!",
                {
                    "username": self.request.user.username,
                    "id": self.request.user.id,
                    "profile_owner": User.objects.get(pk=self.kwargs["pk"]).username,
                    "profile_owner_id": self.kwargs["pk"],
                },
            )
            return render(
                request=request,
                template_name="tutoringApp/forbidden.html",
                status=403,
                context={
                    "warning_message": "You are not allowe to edit other user's profile!",
                    "redirect_link": reverse("home:home"),
                    "redirect_destination": "home page",
                },
            )
        return super().get(request, *args, **kwargs)

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
            LOGGER.warning(
                "Education formset uploaded by %(username)s with id %(id)s contains errors: %(errors)s"
                % {
                    "username": self.request.user.username,
                    "id": self.request.user.id,
                    "errors": filled_education_formset.errors,
                }
            )

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
            LOGGER.warning(
                "User forms uploaded by %(username)s with id %(id)s contains errors: %(errors)s"
                % {
                    "username": self.request.user.username,
                    "id": self.request.user.id,
                    "errors": update_user_form.errors,
                }
            )

    def _remove_info_about_profile_setup_from_sessions(self) -> None:
        """Remove info about whether profile is being set up from session.

        The method attempts to remove the 'profile_setup' key from
        the session object after it has been passed to the context.
        """
        try:
            del self.request.session["profile_setup"]
        except KeyError as e:
            LOGGER.warning(
                'Error when attempting to remove "profile_setup" key from session: %(error)s'
                % {"error": e}
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
    education_id = education.pk
    profile = education.profile
    education.delete()
    LOGGER.debug(
        "Education object with id %(id)s successfuly deleted." % {"id": education_id}
    )
    return HttpResponseRedirect(reverse("profiles:update", kwargs={"pk": profile.pk}))
