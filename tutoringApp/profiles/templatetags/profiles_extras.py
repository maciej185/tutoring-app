from typing import Union

from django import template

register = template.Library()


@register.simple_tag
def formset_error_renderer(
    error_list: Union[list[dict[str, str]], None], form_index: int, field: str
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
