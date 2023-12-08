from .authentication import LoginView, RegisterView, logout_view
from .display import DisplayStudentProfileView, DisplayTutorProfileView
from .update import (
    PasswordChangeView,
    ProfilesPasswordResetCompleteView,
    ProfilesPasswordResetConfirmView,
    ProfilesPasswordResetDoneView,
    ProfilesPasswordResetView,
    UpdateStudentProfileView,
    UpdateTutorProfileView,
    create_profile_view,
)

__all__ = [
    "LoginView",
    "logout_view",
    "RegisterView",
    "create_profile_view",
    "UpdateStudentProfileView",
    "UpdateTutorProfileView",
    "DisplayStudentProfileView",
    "DisplayTutorProfileView",
    "PasswordChangeView",
    "ProfilesPasswordResetView",
    "ProfilesPasswordResetDoneView",
    "ProfilesPasswordResetConfirmView",
    "ProfilesPasswordResetCompleteView",
]
