from .authentication import LoginView, RegisterView, logout_view
from .profile import create_profile_view, delete_education_object_view
from .student import UpdateStudentProfileView

__all__ = [
    "LoginView",
    "logout_view",
    "RegisterView",
    "create_profile_view",
    "UpdateStudentProfileView",
    "delete_education_object_view",
]
