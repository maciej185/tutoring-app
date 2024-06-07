from django.urls import path

from chat import views

app_name = "chat"
urlpatterns = [
    path("tutor/<int:tutor_id>/", view=views.TutorChatView.as_view(), name="tutor_chat"),
    path("tutor/<int:tutor_id>/<int:student_id>/", view=views.TutorChatWindowView.as_view(), name="tutor_chat_window"),
    path("student/<int:student_id>/", view=views.StudentChatView.as_view(), name="student_chat"),
    path("student/<int:tutor_id>/<int:student_id>/", view=views.StudentChatWindowView.as_view(), name="student_chat_window"),
]