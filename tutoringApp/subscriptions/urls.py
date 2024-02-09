from django.urls import path

from . import views

app_name = "subscriptions"
urlpatterns = [
    path(
        "create",
        view=views.CreateSubscriptionView.as_view(),
        name="subscription_create",
    ),
    path(
        "learning/tutor/<int:subscription_id>",
        view=views.LearningTutorView.as_view(),
        name="learning_tutor",
    ),
    path(
        "learning/student/<int:subscription_id>",
        view=views.LearningStudentView.as_view(),
        name="learning_student",
    ),
    path(
        "appointment/create/<int:subscription_id>",
        view=views.create_appointment_view,
        name="appointment_create",
    ),
    path(
        "appointment/delete/<int:pk>",
        view=views.DeleteAppointmentView.as_view(),
        name="appointment_delete",
    ),
]
