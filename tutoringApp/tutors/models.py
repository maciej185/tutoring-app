from datetime import datetime, timedelta

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import Q

from profiles.models import Profile
from tutors.validators import SessionLengthValidator

# Create your models here.


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
        ],
    )
    price_per_hour = models.PositiveIntegerField()
    session_length = models.PositiveIntegerField(
        default=60,
        help_text="Duration of one tutoring session in minutes",
        validators=[
            MinValueValidator(30),
            MaxValueValidator(180),
            SessionLengthValidator,
        ],
    )
    is_default = models.BooleanField(
        default=True,
        help_text="Indicate if its a default, 1 session service that is created when adding the subject when the profile is created.",
    )

    class Meta:
        constraints = [
            # models.UniqueConstraint(fields=["subject", "tutor"], condition=Q(is_default=True), name="one_default", violation_error_message="One default"),
            models.UniqueConstraint(
                fields=["subject", "tutor"],
                condition=Q(number_of_hours=1),
                name="only_default_services_with_1_session",
                violation_error_message="One service with one sessions",
            ),
        ]

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

    @property
    def end(self) -> datetime:
        """Return end time of an available session.

        Returns:
            End time of a session calcualted based on
            `start` field and the value of `session_length`
            fields from the related `Service` object.
        """
        return self.start + timedelta(minutes=self.service.session_length)

    def __str__(self) -> str:
        """String representation fo the model's instance."""
        return f"Availability of {self.service.tutor.user.username} for {self.service.subject.name} sessions."
