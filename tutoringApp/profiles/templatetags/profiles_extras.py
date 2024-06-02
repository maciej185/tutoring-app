from datetime import date, datetime
from typing import Any, Optional

from django import template

from profiles.models import LanguageLevelChoices
from tutors.models import Service

register = template.Library()


@register.simple_tag
def formset_error_renderer(
    error_list: Optional[list[dict[str, str]]], form_index: int, field: str
) -> str:
    """Render correct error message for given field in formset instance.

    Args:
        error_list: A list of dictionaries containing
                    error messages for a given formset
                    instance. The length of the list is
                    equal to the number of forms in a given
                    formset. The keys of these dictionaries
                    are field names of the form and the values
                    are error messages.
        form_index: Index of the form for which the error
                    message will be rendered. Based on this
                    index, correct dictionary gets selected
                    from the error_list.
        field: Name of the field for which the error
                message will be rendered. It is used
                to select a correct value from the dictionary
                selected using value of the form_index argument.

        Returns:
            A string with the error message for the field
            whose name is passed as the value of the 'field'
            attribute selected from the dictionary whose index
            in the 'error_list' is specified in the 'form_index'
            argument.
    """
    if error_list:
        try:
            return (
                error_list[form_index].get(field)[0]
                if error_list[form_index].get(field)
                else ""
            )
        except IndexError:
            return ""
    return ""


@register.simple_tag
def form_error_renderer(error_dict: Optional[dict[str, str]], field: str) -> str:
    """Render correct error message for given field in form instance.

    Args:
        error_dict: A dictionary containing
                    error messages for a given forms
                    instance. The keys of the dictionary
                    are field names of the form and the values
                    are error messages.
        field: Name of the field for which the error
                message will be rendered.

        Returns:
            A string with the error message for the field
            whose name is passed as the value of the 'field'
            argument if error occured, empty string otherwise.
    """
    if error_dict:
        return error_dict.get(field)[0] if error_dict.get(field) else ""
    return ""


def find_same_error_in_both_lists(list1: list[str], list2: list[str]) -> Optional[str]:
    """Check if the same error message is present in both fields.

    The method checks if an error message is present in both
    arrays. If so, the string representing that message
    gets returned.

    Args:
        list1: List containing error messages
                for the first field.
        list2: List containing error messages
                for the second field.

    Returns:
        String representing error message that was
        found in both lists, None if such message
        was not found.
    """
    if len([*list1, *list2]) == len([*{*[*list1, *list2]}]):
        return
    for error in list1:
        if error in list2:
            return error


@register.simple_tag
def education_dates_error_renderer(
    error_dict: list[Optional[dict[str, str]]], form_index: int
) -> str:
    """Renders info about incorrect dates.

    The method checks if the error message for both start_-
    and end_- date fields is the same and if it refers to the
    fact that start_date falls after end_date. If so, that error
    message gets then returned.

    Args:
        error_dict: A dictionary containing
                    error messages for a given forms
                    instance. The keys of the dictionary
                    are field names of the form and the values
                    are error messages.
    Returns:
            A string with the error message informing
            the user about incorrect dates if the error
            did occur, empty string otherwise.
    """
    if not error_dict:
        return ""
    start_date_list = error_dict[form_index].get("start_date")
    end_date_list = error_dict[form_index].get("end_date")
    if not (start_date_list and end_date_list):
        return ""
    error = find_same_error_in_both_lists(list1=start_date_list, list2=end_date_list)
    return error if error else ""


@register.filter(name="subtract")
def subtract(value: str, arg: str) -> int:
    """Subtracts arg from value.

    Args:
        value: The minuend of the operation.
        arg: The subtrahend of the operation.

    Returns:
        Result of the subtraction as an integer.
    """
    return int(value) - int(arg)


@register.simple_tag
def render_experience(teaching_since: Optional[date]) -> str:
    """Calculate given Tutor's experience in years as a string.

    The function calculates the difference between the value
    of the `teaching_since` field from `Profile` model and the
    current time to determine the number of years of experience.

    Args:
        The value of given Tutor's `teaching_since` field,
        None if there was a mistake and an attempt to render
        the page for a Student's profile.

    Returns:
        Given Tutor's experience in years as a string
    """
    if not teaching_since:
        return

    now_date = datetime.now()

    num_months = (now_date.year - teaching_since.year) + (
        now_date.month - teaching_since.month
    )

    if num_months < 12:
        return "Less than one year."
    elif num_months == 12:
        return "1 year."
    elif num_months > 12 and num_months % 12 == 0:
        return f"{num_months % 12} years."
    elif num_months > 12 and num_months % 12 != 0:
        return f"Over { num_months % 12} years."


@register.simple_tag
def redner_language_level(level: int) -> str:
    """Return verbal representation of language level.

    Args:
        level: The value of the `level` field from the
                `ProfileLanguageList` model.
    Returns:
        Verbal representation of language level
    """
    return LanguageLevelChoices(level).label


@register.simple_tag
def render_service_name(service: Service) -> str:
    """Return descriptive name of the service.

    The method checks how many hours are included
    in the given service and based on that information,
    a descriptive name is returned.

    Args:
        service: An instance of the Service model.

    Returns:
        A descriptive name of the given service.
    """
    return (
        f"Single session - {service.subject.name}"
        if service.number_of_hours == 1
        else f"{service.number_of_hours} sessions - {service.subject.name} "
    )


@register.simple_tag
def render_service_price(service: Service) -> int:
    """Calculate price of the entire service.

    The method calculates the entire price
    of the service based on the values of
    `price_per_hour` and `number_of_hours`
    fields.

    Args:
        service: An instance of the Service model.

    Returns:
        Calculated price of the entire service.
    """
    return service.price_per_hour * service.number_of_hours


@register.filter
def dictionary_lookup(
    dictionary: dict[Any, dict[Any, Any]], key: Any
) -> list[tuple[Any]]:
    """Lookup a dictionary value.

    The filter allows to extract items (list of tuples with keys and values) from
    a dictionary that itself is a value of another dict by key of that outer dictionary.

    Args:
        dictionary: Contains another dictionaries as values.
        key: Key of the initial dictionary used to select
            a correct `sub-dicrionary`.

    Returns:
        Result of calling `.items()` method on a `sub-dicrionary` selected
        from the provided, `outer` dicttionary using given key.
    """
    return dictionary.get(key).items()
