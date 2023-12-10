"""URL configuration for tutoringApp project."""

from django.urls import path

from . import views

app_name = "tutors"
urlpatterns = [
    path(
        "availability/<int:pk>/<int:month>/<int:year>",
        view=views.AvailabilityInputView.as_view(),
        name="availability",
    ),
]
