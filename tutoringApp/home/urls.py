from django.urls import path
from . import views

app_name = "home"

urlpatterns = [
    path("", view=views.homeView, name="home")
]