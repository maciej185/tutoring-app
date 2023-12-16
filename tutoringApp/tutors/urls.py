"""URL configuration for tutoringApp project."""

from django.urls import path

from . import views

app_name = "tutors"
api_endpoints = [
    path(
        "availability/delete/<int:pk>",
        view=views.AvailabilityAPIView.as_view(),
        name="availability_delete",
    ),
    path(
        "availability/create",
        view=views.AvailabilityAPIView.as_view(),
        name="availability_create",
    ),
    path(
        "availability/update",
        view=views.AvailabilityAPIView.as_view(),
        name="availability_update",
    ),
]
urlpatterns = [
    path(
        "availability/<int:pk>/<int:month>/<int:year>",
        view=views.AvailabilityInputView.as_view(),
        name="availability",
    ),
    path(
        "services/<int:pk>",
        view=views.ServiceConfigurationView.as_view(),
        name="services",
    ),
    path(
        "service/delete/<int:service_id>",
        view=views.service_delete_view,
        name="service_delete",
    ),
] + api_endpoints
