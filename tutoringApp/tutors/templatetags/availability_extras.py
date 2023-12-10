from datetime import date, datetime
from typing import Optional

from django import template

register = template.Library()


@register.simple_tag
def format_start_time(start_time: datetime) -> str:
    """Format start time of a session into a correct format.

    Return:
        The value of `start` field from the
        `Availability` model in a format that could
        be rendered by an input HTML tag of type `time`.
    """
    return start_time.strftime("%H:%M")


@register.simple_tag
def render_previous_months_day_number(day_number: str) -> str:
    """Format previous months day correctly.

    The method splits the number representing days of the previous months
    that are prefixed with the month's index, separated with an
    underscore.

    Args:
        Day of the previous month prefixed with the
        month's index.

    Returns:
        A number representing given day of a
        previous month.
    """
    return day_number.split("_")[-1]
