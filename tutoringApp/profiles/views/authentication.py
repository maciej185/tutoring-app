"""Views for registering, loggin in and out."""
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpRequest, HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic.edit import FormView

from profiles.forms import LoginForm, RegisterForm, AccountType
from profiles.models import Profile

class LoginView(FormView):
    """Handle logging in of an user."""

    template_name = "profiles/login.html"
    form_class = LoginForm
    success_url = reverse_lazy("home:home")

    def form_valid(self, form):
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        user = authenticate(username=username, password=password)
        if user is not None:
            login(self.request, user)
            self._set_account_type_in_sessions(user=user)
            return super().form_valid(form)
        
    def _set_account_type_in_sessions(self, user: User) -> None:
        """Sets the info about the account type in sessions.
        
        The method sets the necessary info about the account
        type in the self.request.sessions object based on the 
        data provided in the registration form. This information
        is nedeed to decide which page the user should be redirected
        to.

        Args:
            user: An instance of the User object representing the
                    currently loggedn in user.
        """
        profile = Profile.objects.get(user=user)
        self.request.session['account_type'] = AccountType.STUDENT.value if profile.is_student() else AccountType.TUTOR.value


def logout_view(request: HttpRequest) -> HttpResponseRedirect:
    """Logs the user out."""
    logout(request)
    del request.session['account_type']
    return HttpResponseRedirect(reverse_lazy("profiles:login"))


class RegisterView(FormView):
    """Handle registration of new users."""

    template_name = "profiles/register.html"
    form_class = RegisterForm

    def _set_account_type_in_sessions(self, form: RegisterForm) -> None:
        """Sets the info about the account type in sessions.
        
        The method sets the necessary info about the account
        type in the self.request.sessions object based on the 
        data provided in the registration form. This information
        is nedeed to decide which page the user should be redirected
        to.

        Args:
            form: A bound instance of the RegisterForm containing 
                information about the account's type.
        """
        self.request.session['account_type'] = AccountType.STUDENT.value if int(form.cleaned_data.get("account_type")) == AccountType.STUDENT.value else AccountType.TUTOR.value

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        self._set_account_type_in_sessions(form=form)
        return HttpResponseRedirect(reverse_lazy("profiles:create", kwargs={"user_id": user.pk}))
