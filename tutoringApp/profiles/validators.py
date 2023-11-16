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
