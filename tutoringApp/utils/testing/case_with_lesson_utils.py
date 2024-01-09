"""Extenstion of TestCaseBookingeUtils allowing to create mock Lesson-related objects."""

from datetime import datetime, timedelta, timezone

from freezegun import freeze_time

from django.core.files import File

from lessons.models import Lesson, Task, Material
from profiles.models import Profile
from tutors.models import Availability

from .case_with_booking_utils import TestCaseBookingeUtils, NOW

import tempfile

DEFAULT_TASK_DUE_DATE = datetime.fromisoformat(NOW) + timedelta(days=1)

class TestCaseLessonsUtils(TestCaseBookingeUtils):
    """Extension of TestCaseBookingeUtils class to add method for creating Lesson-related objects."""

    @freeze_time(NOW)
    def setUp(cls):
        """Initial database setup."""
        super().setUp()
        
        cls._register_user("student1")
        student1 = Profile.objects.get(user__username="student1")

        availability = Availability.objects.get(pk=1)
        cls._create_booking_object(availability=availability, student=student1)

    @staticmethod
    @freeze_time(NOW)
    def _create_task_object(lesson: Lesson, title: str, description: str, due_data: datetime = DEFAULT_TASK_DUE_DATE) -> Task:
        """Create a Mock instance of the Task model.
        
        Args:
            lesson: In instance of the Lesson model that 
                    the newly created Task object will be 
                    related to.
            title: Desired value of the `Task.title` field.
            due_date: Desired value of the `Task.due_date` field.
            description: Desired value of the `Task.description` field.

        Returns:
            A newly created Task model instance with provided
            values.
        """
        task = Task(
            lesson=lesson,
            title=title,
            due_date=due_data,
            description=description,
        )
        task.save()
        return task
    
    @staticmethod
    @freeze_time(NOW)
    def _create_material_object(lesson: Lesson, name: int) -> Material:
        """Create a Mock instance of the Material model.
        
        Args:
            lesson: An instance of the Lesson model that 
                    the newly created Material object will be 
                    related to.
            name: Desired value of the `Material.name` field.
    
        Returns:
            A newly created mock Material model instance.
        """
        f = tempfile.NamedTemporaryFile(suffix=".pdf")
        f.write(b"Mock file content.")
        material = Material.objects.create(
            lesson=lesson,
            name=name,
            file=File(file=f),
        )
        material.save()
        f.close()
        
        return material
