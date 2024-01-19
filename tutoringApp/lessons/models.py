from datetime import timedelta
from pathlib import Path
from typing import Union

from django.db import models
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _

from lessons.validators import MaterialFileExtensionValidator
from profiles.models import Profile
from tutors.models import Availability, Service

# Create your models here.


class LessonStatusChoices(models.IntegerChoices):
    """Enumerated integer choices for lessons's status."""

    HAVE_NOT_TAKEN_PLACE = 0, _("Have not taken place")
    CURRENTLY_TAKING_PLACE = 1, _("Currently taking place")
    TOOK_PLACE = 2, _("Took place already")


class Lesson(models.Model):
    """Model for storing lesson information.

    Instances of the model store information
    about a single tutoring session and could
    be linked to both single sessions as well
    as an appointment in a continuation of
    series of meetings between Tutor and
    Student (in a case where the Student is
    `Subscribed` to the Tutor).
    """

    date = models.DateTimeField(default=now)
    subject = models.CharField(max_length=250, default="")
    subject_details = models.CharField(max_length=250, default="")
    title = models.CharField(max_length=250, default="")
    absence = models.BooleanField(
        default=False,
        help_text="Indiciates whether Student showed up for the session or not.",
    )

    @property
    def status(self) -> int:
        """Represent Lesson's status.

        The property informs whether the Lessons
        has already took place, will take place
        or is currently taking place. The status
        is calculated based on current time and
        the value of the `date` field.

        Returns:
            An appropriate integer value representing
            the Lesson's status taken from the
            LessonStatusChoices enumerated string class.
        """
        service = self._get_related_service()
        end_date = self.date + timedelta(minutes=service.session_length)
        if now() < self.date < end_date:
            return LessonStatusChoices.HAVE_NOT_TAKEN_PLACE.value
        elif self.date < now() < end_date:
            return LessonStatusChoices.CURRENTLY_TAKING_PLACE.value
        if self.date < end_date < now():
            return LessonStatusChoices.TOOK_PLACE.value

    def __str__(self) -> str:
        """String representation of the Lesson object."""
        return f"Lesson on {self.date} with subject: {self.subject}"

    def _get_related_service(self) -> Service:
        """Fetch related Service object.

        Returns:
            Related Service object, fetched differently
            depending on whether the current Lesson instance
            is related to a Booking or an Appointment.
        """
        try:
            booking = Booking.objects.get(lesson_info=self)
            return booking.availability.service
        except Booking.DoesNotExist:
            return


class Booking(models.Model):
    """Model for storing booked session information.

    Instances of the model store information
    about a booking of a single tutoring
    session. The session is booked by a Student
    based on availability of the Tutor given
    for one of the default Service objects
    (services with 1 as the value of `number_of_hours`
    field)
    """

    lesson_info = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    student = models.ForeignKey(Profile, on_delete=models.CASCADE)
    availability = models.OneToOneField(Availability, on_delete=models.CASCADE)
    create_date = models.DateTimeField(default=now)

    def __str__(self) -> str:
        """String representation that includes info about the lesson and involved users."""
        return f"Session booked by {self.student.user.username} (id: {self.student.user.pk}) with tutor {self.availability.service.tutor.user.username} (id: {self.availability.service.tutor.user.pk}) under Availability with id {self.availability.pk}"


class TaskStatusChoices(models.IntegerChoices):
    """Enumerated integer choices for task's status."""

    SOLUTION_PENDING = 0, _("Solution pending")
    SOLUTION_UPLOADED = 1, _("Solution uploaded")
    SOLUTION_APPROVED = 2, _("Done")
    SOLUTION_DISMISSED = 3, _("Solution dismissed")


class Task(models.Model):
    """Model for storing information about a single task.

    Instances of the model store information about a task
    created by a Tutor, related to one tutoring
    session.
    """

    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    status = models.IntegerField(choices=TaskStatusChoices.choices, default=0)
    title = models.CharField(max_length=250)
    description = models.TextField(max_length=1000)
    due_date = models.DateTimeField()

    def __str__(self) -> str:
        """String representation of a single Task."""
        return f"Task under lesson with ID {self.lesson.pk} due on {self.due_date}"


def get_file_path(instance: Union["Material", "Solution"], filename: str) -> Path:
    """Returns directory where the uploaded file will be stored.

    Args:
        instance: An instance of the model where the FileField is defined.
                    More specifically, this is the particular instance
                    where the current file is being attached.
        filename: The filename that was originally given to the file.

    Returns:
        Path to the destination where the file will be saved
        that is relative to the MEDIA_ROOT directory from
        settings.py file.
    """
    if isinstance(instance, Material):
        return Path(
            "files", "lessons", "materials", f"lesson_{instance.lesson.pk}", filename
        )
    elif isinstance(instance, Solution):
        return Path(
            "files",
            "lessons",
            "tasks",
            f"task_{instance.task.pk}",
            "solution",
            filename,
        )


class Solution(models.Model):
    """Model for storing information about task's solutuion.

    Instances of the model store information about a
    single solution to a task uploaded by a Student
    assigned to the given tutoring session.
    """

    task = models.OneToOneField(Task, on_delete=models.CASCADE)
    solution = models.FileField(
        upload_to=get_file_path,
        max_length=250,
    )
    upload_date = models.DateTimeField(default=now)

    def __str__(self) -> str:
        """String representation of a Task's solution."""
        return (
            f"Solution to a task with ID {self.task.pk} uploaded on {self.upload_date}"
        )


class Material(models.Model):
    """Model for storing information about sessions's materials.

    Instances of the model store information about
    materials (notes, summaries, textbook fragments)
    related to a single tutoring session.
    """

    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    name = models.CharField(max_length=250)
    file = models.FileField(
        upload_to=get_file_path,
        max_length=250,
        validators=[MaterialFileExtensionValidator],
    )
    upload_date = models.DateTimeField(default=now)

    def __str__(self) -> str:
        """String representation of a Material object."""
        return f"Learnign material attached to a Lesson (id: {self.lesson.pk}) with a name of: {self.name}."


class Entry(models.Model):
    """Model for storing information about session's entry.

    Instances of the model store information about
    entries related to a given tutoring session.
    These could be comments, questions, reminders
    from both Tutor and/or Student.
    """

    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    from_student = models.BooleanField(default=True)
    text = models.TextField(max_length=1000)
    publish_date = models.DateTimeField(default=now)

    def __str__(self) -> str:
        """String representation of single Lesson's entry."""
        return f"Entry {'from Student' if self.from_student else 'from Tutor'} under Lesson with id {self.lesson.id} published on {self.publish_date}"
