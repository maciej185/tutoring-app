from django.urls import path

from lessons import views

app_name = "lessons"
api_endpoints = [
    path(
        "solution/create",
        view=views.SolutionAPIView.as_view(),
        name="solution_create",
    ),
    path(
        "solution/delete/<int:pk>",
        view=views.SolutionAPIView.as_view(),
        name="solution_delete",
    ),
    path(
        "task/update/<int:pk>",
        view=views.TaskAPIView.as_view(),
        name="task_update",
    ),
    path(
        "absence/update/<int:pk>",
        view=views.update_lesson_absence_view,
        name="lesson_update_absence",
    ),
]
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
    path(
        "update/<int:pk>",
        view=views.UpdateLessonView.as_view(),
        name="lesson_update",
    ),
    path(
        "task/delete/<int:task_id>",
        view=views.delete_task_view,
        name="task_delete",
    ),
    path(
        "material/delete/<int:material_id>",
        view=views.delete_material_view,
        name="material_delete",
    ),
    path(
        "student/<int:pk>",
        view=views.DisplayLessonStudentView.as_view(),
        name="lesson_display_student",
    ),
    path(
        "tutor/<int:pk>",
        view=views.DisplayLessonTutorView.as_view(),
        name="lesson_display_tutor",
    ),
] + api_endpoints
