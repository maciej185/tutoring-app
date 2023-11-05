from django.urls import path

from . import views

app_name = "profiles"
urlpatterns = [
    path("login/", view=views.LoginView.as_view(), name="login"),
    path("logout/", view=views.logout_view, name="logout"),
]
