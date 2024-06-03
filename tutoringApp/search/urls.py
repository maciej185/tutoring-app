from django.urls import path

from . import views

app_name = "search"
urlpatterns = [
    path("student", view=views.StudentSearchResultsView.as_view(), name="for_student"),
]
