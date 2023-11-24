from pathlib import Path

from django.conf import settings
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _
from simple_history.models import HistoricalRecords

from profiles.validators import FileSizeValidator, SessionLengthValidator


def profile_pic_directory_path(instance: "Profile", filename: str) -> Path:
    """Return path for uploading User's profile picture.

    Args:
        instance: An instance of the model where the ImageField is defined.
        filename: The filename that was originally given to the file.
    Returns:
        A part of a path that will be appended to the MEDIA_ROOT
        path (defined in settings.py) to determine the final
        directory where the image will be saved.
    """
    return Path(
        "media",
        "profiles",
        "images",
        f"user_{instance.user.id}",
        "profile_pic",
        filename,
    )


# Create your models here.
class Profile(models.Model):
    """Implementation of the Profile Model.

    The Model can be used to create both Tutors'
    and Student's profiles as most of the information
    is shared between the two entites. The only
    exception is the 'teaching_since' field.
    When the value of this field is equal to
    Null/None, the profile is a Student's profile.
    """

    DEFAULT_PROFILE_PIC_PATH = Path(
        settings.BASE_DIR, "media", "default_profile_pic.jpg"
    )

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    profile_pic = models.ImageField(
        upload_to=profile_pic_directory_path,
        default=str(DEFAULT_PROFILE_PIC_PATH),
        null=False,
        blank=False,
        validators=[FileSizeValidator],
    )
    date_of_birth = models.DateField(blank=False, default=now)
    description = models.TextField(blank=False, default="")
    city = models.CharField(max_length=100, blank=False, default="")
    teaching_since = models.DateField(
        null=True,
        blank=True,
        help_text="If the instance is Student's profile then this field must be Null.",
    )
    create_date = models.DateTimeField(default=now)
    timestamp = models.DateTimeField(auto_now=True)
    languages = models.ManyToManyField("Language", through="ProfileLanguageList")
    schools = models.ManyToManyField("School", through="Education")
    history = HistoricalRecords()

    def is_student(self) -> bool:
        """Returns boolean info whether given profile is a Student's profile.

        The method checks the value of the 'teaching_since' field to determine
        whether the profile belongs to a Student.
        """
        return True if self.teaching_since is None else False

    def __str__(self) -> str:
        """Returns info about profile that includes the username."""
        return f"{self.user.username}'s profile"


class Language(models.Model):
    """Model for storing available languages.

    The user will be able to select values
    from this model in the 'Languages' section
    when creating a profile. The values for this
    model can only be inserted/changed/deleted by
    an admin.
    """

    name = models.CharField(max_length=100)

    def __str__(self) -> str:
        """Return the language name as its representation."""
        return self.name


class ProfileLanguageList(models.Model):
    """An intermediate table between Profile and Language models.

    The table is meant to be used to connect Profile and
    Language models using ManyToManyField and allowing to
    provide additonal infromation about the user's proficiency
    in that language."""

    LANGUAGE_LEVEL_CHOICES = [
        (0, "Beginner"),
        (1, "Elementary"),
        (2, "Intermediate"),
        (3, "Upper Intermediate"),
        (4, "Advanced"),
        (5, "Native"),
    ]

    language = models.ForeignKey(Language, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    level = models.IntegerField(choices=LANGUAGE_LEVEL_CHOICES, default=0)


class School(models.Model):
    """Model for storing available school choices.

    The user will be able to select schools
    from this model in the 'Education' section
    when creating a profile. The values for this
    model can only be inserted/changed/deleted by
    an admin.
    """

    SCHOOL_LEVEL_CHOICES = [
        (0, "Elementary School"),
        (1, "Middle School"),
        (2, "High School"),
        (3, "College"),
        (4, "University"),
    ]
    name = models.CharField(max_length=200, unique=True)
    level = models.IntegerField(choices=SCHOOL_LEVEL_CHOICES, default=0)
    country = models.CharField(max_length=100)
    city = models.CharField(max_length=100)

    def __str__(self) -> str:
        """Return the school's name as its representation."""
        return self.name


class Education(models.Model):
    """An intermediate table between Profile and School models.

    The table is meant to be used to connect Profile and
    School models using ManyToManyField. Using an intermediate table
    allows to provide additional information about the type of degree,
    dates of attandence and any additional, relevant info.
    """

    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    degree = models.CharField(max_length=100)
    additional_info = models.CharField(
        max_length=250, help_text="GPA, awards, associations etc."
    )


class Subject(models.Model):
    """Model for storing available Subject.

    Tutors will be able to select a subject
    from the list of instances of this model
    to configure the services that they are
    offering. The instances of this model
    are not to be created by the users,
    only by the staff.
    """

    SUBJECT_CATEGORY_CHOICES = [
        (0, "Languages"),
        (1, "Science"),
        (2, "Maths"),
        (3, "Arts and humanities"),
        (4, "Social sciences"),
    ]

    name = models.CharField(max_length=250)
    category = models.IntegerField(choices=SUBJECT_CATEGORY_CHOICES)

    def __str__(self) -> str:
        """String representation fo the model's instance."""
        return self.name


class Service(models.Model):
    """Model for storing info about services offered by a Tutor.

    Tutors are be able to configure "bundles" of sessions
    in a so called Service. Service stores information
    about the subject that is taught in the sessions,
    the number of sessions offered, price per hour as
    well as the duration of one session.
    """

    tutor = models.ForeignKey(Profile, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    number_of_hours = models.PositiveIntegerField(
        default=1,
        validators=[
            MinValueValidator(1),
            MaxValueValidator(100),
            SessionLengthValidator,
        ],
    )
    price_per_hour = models.PositiveIntegerField()
    session_length = models.PositiveIntegerField(
        default=60,
        help_text="Duration of one tutoring session in minutes",
        validators=[MinValueValidator(30), MaxValueValidator(180)],
    )
    is_default = models.BooleanField(
        default=True,
        help_text="Indicate if its a default, 1 session service that is created when adding the subject when the profile is created.",
    )

    def __str__(self) -> str:
        """String representation fo the model's instance."""
        return f"{self.subject.name} taught by {self.tutor.user.username}"


class Availability(models.Model):
    """Store Tutor's availability for given Service.

    Tutors are able to input their availability for
    different services by simply providing the start
    time. The end of the given session is calculated
    based on the session length.
    """

    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    start = models.DateTimeField()

    def __str__(self) -> str:
        """String representation fo the model's instance."""
        return f"Availability of {self.service.tutor.user.username} for {self.service.subject.name} sessions."
