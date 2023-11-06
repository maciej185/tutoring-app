from django.contrib.auth import authenticate, login, logout
from django.http import HttpRequest, HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic.edit import FormView

from profiles.forms import LoginForm, RegisterForm


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
            return super().form_valid(form)


def logout_view(request: HttpRequest) -> HttpResponseRedirect:
    """Logs the user out."""
    logout(request)
    return HttpResponseRedirect(reverse_lazy("profiles:login"))


class RegisterView(FormView):
    """Handle registration of new users."""

    template_name = "profiles/register.html"
    form_class = RegisterForm

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return HttpResponseRedirect(reverse_lazy("home:home"))
