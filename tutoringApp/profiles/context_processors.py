"""Custom context processors for profile app."""
from django.core.cache import cache
from django.http import HttpRequest

from profiles.forms import AccountType
from profiles.models import Profile
from tutors.models import Subject


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
        except (TypeError, Profile.DoesNotExist):
            is_student = None
    else:
        is_student = None
    return {"is_student": is_student}


def add_subjects(request: HttpRequest) -> dict[str, list[str]]:
    """Add all the available subjects to the context.

    The processor first checks if the currently logged in user is a
    Student and if so, it retrieves all the available Subjects
    from the database so that they could be used as a search criteria
    in the search bar at the top of the page. The processor uses
    caching to avoid making calls to the database on every request.

    Args:
        request: An instance of the HttpRequest, containing
                    information about the request sent by the user.

    Returns:
       A dictionary with the list of all available Subjects.
    """
    account_type_dict = add_account_type(request=request)
    if not account_type_dict:
        return {"subjects": None}
    if not account_type_dict["is_student"]:
        return {"subjects": None}

    cached_subjects = cache.get("subjects")
    if not cached_subjects:
        subjects = Subject.objects.all()
        cache.set("subjects", subjects, 1 * 24 * 60 * 60)
        return {"subjects": subjects}
    return {"subjects": cached_subjects}
