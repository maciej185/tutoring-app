"""Validators for models in `tutors` app."""
from django.core.exceptions import ValidationError


def SessionLengthValidator(session_length: int) -> None:
    """Ensure session lengths are multiples of 15.

    Args:
         session_length: Tutoring session's length in minutes.

    Raises:
        ValidationError -  raised when provided value of session
                            length is not a multiple of 15.
    """
    if session_length % 15 != 0:
        raise ValidationError("The session length must be a multiple of 15!")
