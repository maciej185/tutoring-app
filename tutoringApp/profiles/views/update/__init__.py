from .password_change import PasswordChangeView
from .password_reset import (
    ProfilesPasswordResetCompleteView,
    ProfilesPasswordResetConfirmView,
    ProfilesPasswordResetDoneView,
    ProfilesPasswordResetView,
)
from .update import create_profile_view
from .update_student import UpdateStudentProfileView
from .update_tutor import UpdateTutorProfileView

__all__ = [
    "UpdateStudentProfileView",
    "UpdateTutorProfileView",
    "create_profile_view",
    "PasswordChangeView",
    "ProfilesPasswordResetView",
    "ProfilesPasswordResetDoneView",
    "ProfilesPasswordResetConfirmView",
    "ProfilesPasswordResetCompleteView",
]
