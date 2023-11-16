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
