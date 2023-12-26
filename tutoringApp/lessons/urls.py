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
]
