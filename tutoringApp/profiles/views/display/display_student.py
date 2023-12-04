"""Views for displaying Students' profile information."""
from profiles.forms import AccountType

from .display import DisplayProfileView


class DisplayStudentProfileView(DisplayProfileView):
    """Display Students' profile information."""

    def get_template_names(self) -> list[str]:
        """Decide which template to display based on the current user's profile type."""
        account_type = self.request.session.get("account_type")
        return (
            "profiles/display_student_4_tutor.html"
            if account_type == AccountType.TUTOR.value
            else "profiles/display_student_4_student.html"
        )
