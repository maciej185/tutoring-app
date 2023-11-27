from logging import getLogger
from typing import Union

from django.forms.models import BaseModelForm
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse_lazy

from .profile import UpdateProfileView

LOGGER = getLogger(__name__)


class UpdateStudentProfileView(UpdateProfileView):
    """Class for updating Student's Profile."""

    template_name = "profiles/update_student.html"

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
            LOGGER.debug(
                "Profile of user %(username)s with id %(id)s successfuly updated.",
                {"username": self.request.user.username, "id": self.request.user.id},
            )
            return super().form_valid(form)
        return HttpResponseRedirect(
            reverse_lazy("profiles:student_update", kwargs={"pk": self.kwargs["pk"]})
        )
