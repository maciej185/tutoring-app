"""Custom context processors for profile app."""
from django.http import HttpRequest


def add_profile_pic_url_processor(request: HttpRequest) -> dict[str, str]:
    """Add current user's profile picture URL to context.

    The method checks if the info about current user's profile
    picture is present in the session info and if so, it gets
    added to the context.

    Args:
        request: An instance of the HttpRequest, containing
                    information about the request sent by the user.
    """
    return (
        {"profile_pic_url": request.session.get("profile_pic_url")}
        if request.session.get("profile_pic_url")
        else {}
    )
