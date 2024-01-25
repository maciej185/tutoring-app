"""Custom filters and tags for the `subscriptions` app."""
from datetime import timedelta

from django import template

from lessons.models import Lesson
from subscriptions.models import Appointment, ServiceSubscriptionList

register = template.Library()


@register.simple_tag
def render_lessons_timeslot(lesson: Lesson) -> str:
    """Render given Lesson's time slot.

    Args:
        lesson: Intance of the Lesson object for which the time
        slot will be rendered.
    Returns:
        A string representing the Lesson's time slot in the
        format of: '[date], [start time] - [end time]'.
    """
    appointment = Appointment.objects.get(lesson_info=lesson)
    service = ServiceSubscriptionList.objects.get(appointment=appointment).service
    end_time = lesson.date + timedelta(minutes=service.session_length)
    return f"{lesson.date.strftime('%d. %b %Y')}, {lesson.date.strftime('%H:%M')} - {end_time.strftime('%H:%M')}"
