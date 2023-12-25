from django import template

from lessons.models import Booking
from tutors.models import Availability

register = template.Library()


@register.simple_tag
def render_availability_time_slot(availability: Availability) -> str:
    """Render Availability time slot in human-readable format.

    Args:
        availability: Instance of the Availability model whose time
                        slot is meant to be rendered.

    Returns
        Availability time slot formatted as a string.
    """
    return f"{availability.start.strftime(r'%d. %b %Y, %H:%M')}-{availability.end.strftime(r'%H:%M')}"


@register.simple_tag
def render_booking_title(booking: Booking, is_student: bool) -> int:
    """Render booking's title.

    The tag renders booking title with different
    information about the session's participant
    depending on whether the page is displayed by a
    Tutor or Student and the related Lesson's title.

    Args:
        booking: Instance of the Booking model
                    whose title is meant to be rendered.
        is_student: Boolean information about whether
                    the Booking's title should be displayed
                    for a Student.
    """
    booking_title = (
        booking.lesson_info.title
        if booking.lesson_info.title
        else f"Single {booking.availability.service.subject} session"
    )
    participant = (
        booking.availability.service.tutor.user.username
        if is_student
        else booking.student.user.username
    )
    return f"{booking_title} with {participant}"
