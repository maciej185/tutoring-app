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
        "learning/tutor",
        view=views.ListSubscriptionsTutorView.as_view(),
        name="learning_tutor_list",
    ),
    path(
        "learning/tutor/<int:subscription_id>",
        view=views.LearningTutorView.as_view(),
        name="learning_tutor",
    ),
    path(
        "learning/student",
        view=views.ListSubscriptionsStudentView.as_view(),
        name="learning_student_list",
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
    path(
        "review/create/<int:subscription_id>",
        view=views.CreateReviewView.as_view(),
        name="review_create",
    ),
    path(
        "review/delete/<int:review_id>",
        view=views.DeleteReviewView.as_view(),
        name="review_delete",
    ),
]
