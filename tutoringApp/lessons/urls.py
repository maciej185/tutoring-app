from django.urls import path

from lessons import views

app_name = "lessons"
urlpatterns = [
    path(
        "booking/create/<int:availability_id>",
        view=views.create_booking_view,
        name="booking_create",
    ),
    path(
        "booking/display/student",
        view=views.BookingsDisplay4Student.as_view(),
        name="booking_display_student",
    ),
    path(
        "booking/display/tutor",
        view=views.BookingsDisplay4Tutor.as_view(),
        name="booking_display_tutor",
    ),
    path(
        "booking/delete/<int:pk>",
        view=views.BookingDeleteView.as_view(),
        name="booking_delete",
    ),
]
