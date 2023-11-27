from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import UploadedFile


def FileSizeValidator(file: UploadedFile) -> None:
    """Raises ValidationError when the upload file exceeds the limit.

    Args:
        file: An instance of the UploadedFile class representing
            the actual file uploaeded by the user.

    Raises:
        ValidationError - raised when file exceeds size limit.
    """

    limit = 1024 * 1024
    if file.size > limit:
        raise ValidationError("File too large. Size should not exceed 1 MB.")


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
