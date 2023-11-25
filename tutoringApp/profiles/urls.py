from django.urls import path

from . import views

app_name = "profiles"
urlpatterns = [
    path("login/", view=views.LoginView.as_view(), name="login"),
    path("logout/", view=views.logout_view, name="logout"),
    path("register/", view=views.RegisterView.as_view(), name="register"),
    path("create/<int:user_id>", view=views.create_profile_view, name="create"),
    path(
        "student/update/<int:pk>",
        view=views.UpdateStudentProfileView.as_view(),
        name="student_update",
    ),
    path(
        "education/delete/<int:pk>",
        view=views.delete_education_object_view,
        name="education_delete",
    ),
]
