"""Custom context processors for profile app."""
from django.http import HttpRequest

from profiles.forms import AccountType
from profiles.models import Profile


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


def add_account_type(request: HttpRequest) -> dict[str, bool]:
    """Add current user's account type to the context.

    The method attempts to fetch the account type from the context
    and if it fails (the session timed out for example) the type is
    determined based on the `.user` attribute of the `request` argument.

    Args:
        request: An instance of the HttpRequest, containing
                    information about the request sent by the user.

    Returns:
        A dictionary containing boolean information about whether
        the currently logged in user is a Student or not.
    """
    if request.session.get("account_type"):
        is_student = request.session.get("account_type") == AccountType.STUDENT.value
    elif request.user:
        try:
            profile = Profile.objects.get(user=request.user)
            is_student = profile.is_student()
            request.session["account_type"] = (
                AccountType.STUDENT.value if is_student else AccountType.TUTOR.value
            )
        except TypeError:
            is_student = None
    else:
        is_student = None
    return {"is_student": is_student}
