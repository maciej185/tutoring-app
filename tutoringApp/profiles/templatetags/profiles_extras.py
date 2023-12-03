from typing import Optional

from django import template

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
        return (
            error_list[form_index].get(field)[0]
            if error_list[form_index].get(field)
            else ""
        )
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
