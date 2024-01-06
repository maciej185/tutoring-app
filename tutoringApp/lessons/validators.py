"""Validators for the `lessons` app."""
from pathlib import Path

from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import UploadedFile
from django.utils.translation import gettext_lazy as _


def MaterialFileExtensionValidator(file: UploadedFile) -> None:
    """Ensure file's extension is allowed.

    Args:
        file: An instance of the UploadedFile class representing
            the actual file uploaeded by the user.

    Raises:
        ValidationError - raised when extension is not included
                        in allowed extensions.
    """
    allowed_extensions = [
        ".pdf",
        ".jpg",
        ".png",
        ".gif",
        ".txt",
        ".doc",
        ".docx",
        ".xlsx",
        ".xls",
        ".csv",
    ]
    extension = Path(file.name).suffix
    if not extension in allowed_extensions:
        raise ValidationError(
            _(
                "Incorrect file extensions. Allowed extensions are: %(allowed_extensions)s"
            ),
            code="incorrect_extension",
            params={"allowed_extensions": ", ".join(allowed_extensions)},
        )
