from django.db import models
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _

from lessons.models import Lesson
from profiles.models import Profile
from tutors.models import Service, Subject

# Create your models here.


class Subscription(models.Model):
    """Implementation of the Subscription model.

    The Subscription assigns a Student to a Tutor
    allowing them to purchase non-default
    Services offered by the Tutor and publish
    Reviews on the Tutor's profile.
    """

    tutor = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name="subscription_tutor"
    )
    student = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name="subscription_student"
    )
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    start_date = models.DateTimeField(default=now)

    def __str__(self) -> str:
        """String representation of the class."""
        return f"Student {self.student.user.first_name} {self.student.user.last_name} assigned to {self.tutor.user.first_name} {self.tutor.user.last_name} in {self.subject.name}."

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["tutor", "student", "subject"],
                name="unique_tutor_student_subject_combination",
                violation_error_message="Subscription for this Student and Subject already exists.",
            )
        ]


class ServiceSubscriptionList(models.Model):
    """Intermediate table between Service and Subscription models.

    The models stores information about which Services were
    purchased as part of the Subscription.
    """

    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    subscription = models.ForeignKey(Subscription, on_delete=models.CASCADE)
    purchase_date = models.DateTimeField(default=now)

    def __str__(self) -> str:
        """String representation of the class."""
        return f"Service with ID {self.service.pk} purchased as part of a Subscription with ID {self.subscription.pk}"


class Appointment(models.Model):
    """Intermediate table between ServiceSubscriptionList and Lesson models.

    The model connects the two tables and thus allows
    to create lessons as part of the available hours
    count in the given Subscription.
    """

    subscription_service = models.ForeignKey(ServiceSubscriptionList, on_delete=models.CASCADE)
    lesson_info = models.ForeignKey(Lesson, on_delete=models.CASCADE)

    def __str__(self) -> str:
        """String representation of the class."""
        return f"Appointment as part of a Subscriptio with ID {self.subscription.pk} at {self.lesson_info.date}"


class Review(models.Model):
    """Implementation of the Review model.

    Instances of the model store information
    about the Student's review of the Tutor
    related to a given Subscription.
    """

    subscription = models.OneToOneField(Subscription, on_delete=models.CASCADE)
    star_rating = models.FloatField()
    text = models.TextField()
    publish_date = models.DateTimeField(default=now)

    def __str__(self) -> str:
        """String representation of the class."""
        return f"Review of {self.subscription.tutor.user.first_name} {self.subscription.tutor.user.last_name} teaching {self.subscription.subject.name} by {self.subscription.student.user.first_name} {self.subscription.student.user.last_name}"
