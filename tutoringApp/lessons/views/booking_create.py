"""Views for managin Booking objects."""
from logging import getLogger
from typing import Optional

from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from lessons.models import Booking, Lesson
from profiles.models import Profile
from tutors.models import Availability

LOGGER = getLogger(__name__)


def user_is_tutor_error(
    request: HttpRequest, availability_id: int
) -> Optional[HttpResponse]:
    """Check if the currently logged in user is a Tutor.

    Args:
        request: An instance of the HttpRequest class, containing
                every information about the request sent to the server.
        availability_id: Primary key of the Availability object that the
                Booking will be related to.

    Returns:
        Instance of the HttpResponse class with warning page rendered
        if the currently logged in user is a Tutor, None otherwise.
    """
    profile = Profile.objects.get(user=request.user)
    if not profile.is_student():
        LOGGER.warning(
            "Tutor %(username)s with id %(id)s attempting to book a session under Availabilit with id %()s",
            {
                "username": request.user.username,
                "id": request.user.id,
                "availability_id": availability_id,
            },
        )
        return render(
            request=request,
            template_name="tutoringApp/forbidden.html",
            status=403,
            context={
                "warning_message": "Tutors are not allowed to book sessions with other tutors.",
                "redirect_link": reverse("home:home"),
                "redirect_destination": "home page",
            },
        )


def availability_object_does_not_exist_error(
    request: HttpRequest, availability_id: int
) -> Optional[HttpResponse]:
    """Check if Availability object with provided ID does exist.

    Args:
        request: An instance of the HttpRequest class, containing
                    every information about the request sent to the server.
        availability_id: Primary key of the Availability object that the
                    Booking will be related to.

    Returns:
        Instance of the HttpResponse class with warning page rendered
        if the Availability object with provided ID does not exist,
        None otherwise.
    """
    try:
        Availability.objects.get(pk=availability_id)
    except Availability.DoesNotExist:
        return render(
            request=request,
            template_name="tutoringApp/forbidden.html",
            status=404,
            context={
                "warning_message": "Availability object with provided primary key does not exist.",
                "redirect_link": reverse("home:home"),
                "redirect_destination": "home page",
            },
        )


def booking_relating_to_availability_already_exists_error(
    request: HttpRequest, availability_id: int
) -> Optional[HttpResponse]:
    """Check if a Booking relating to Availability with given ID already exists.

    Args:
        request: An instance of the HttpRequest class, containing
                    every information about the request sent to the server.
        availability_id: Primary key of the Availability object that the
                    Booking would be related to.

    Returns:
        Instance of the HttpResponse class with warning page rendered
        if the Booking realting to given Availability alreasy exists,
        None otherwise.
    """
    availability = Availability.objects.get(pk=availability_id)
    try:
        Booking.objects.get(availability=availability)
        return render(
            request=request,
            template_name="tutoringApp/forbidden.html",
            status=404,
            context={
                "warning_message": "Booking related to Availability with provided ID already exists.",
                "redirect_link": reverse(
                    "profiles:tutor_display",
                    kwargs={"pk": availability.service.tutor.pk},
                ),
                "redirect_destination": "tutor's profile",
            },
        )
    except Booking.DoesNotExist:
        return None


def availability_is_outdated_error(
    request: HttpRequest, availability_id: int
) -> Optional[HttpResponse]:
    """Check if the Availability object with given ID is outdated.

    Args:
        request: An instance of the HttpRequest class, containing
                    every information about the request sent to the server.
        availability_id: Primary key of the Availability object that the
                    Booking would be related to.

    Returns:
        Instance of the HttpResponse class with warning page rendered
        if the given Availability object is outdated, None otherwise.
    """
    availability = Availability.objects.get(pk=availability_id)
    if availability.is_outdated:
        return render(
            request=request,
            template_name="tutoringApp/forbidden.html",
            status=403,
            context={
                "warning_message": "Availability is outdated. Please choose another available time slot.",
                "redirect_link": reverse(
                    "profiles:tutor_display",
                    kwargs={"pk": availability.service.tutor.pk},
                ),
                "redirect_destination": "tutor's profile",
            },
        )


@login_required
def create_booking_view(request: HttpRequest, availability_id: int) -> HttpResponse:
    """Create Booking and corresponding Lesson object.

    The view checks if the request sent is a POST or GET request.
    In case of both request tyoes several checking functions are
    invoked to see if the data and requestor are allowed. If there
    are no errors, different request types result in different behaviors:
        - In case of GET, a confirmation page is displayed.
        - In case of POST, a Booking object is created.

    Args:
        request: An instance of the HttpRequest class, containing
                every information about the request sent to the server.
        availability_id: Primary key of the Availability object that the
                Booking will be related to.

    Returns:
        Instance of the HttpResponse class with rendered warning messages
        in case of errors. If there are no errors, GET request results in
        a response with confirmation page. In case of POST, the Student is
        redirected to their profile page.

    """
    error_checking_functions = [
        user_is_tutor_error,
        availability_object_does_not_exist_error,
        booking_relating_to_availability_already_exists_error,
        availability_is_outdated_error,
    ]
    if request.method == "GET":
        for error_checking_function in error_checking_functions:
            error_res = error_checking_function(request, availability_id)
            if error_res:
                return error_res
        availability = Availability.objects.get(pk=availability_id)
        return render(
            request,
            "booking/create.html",
            context={
                "availability": availability,
                "tutor_profile": reverse(
                    "profiles:tutor_display",
                    kwargs={"pk": availability.service.tutor.pk},
                ),
            },
        )
    elif request.method == "POST":
        for error_checking_function in error_checking_functions:
            error_res = error_checking_function(request, availability_id)
            if error_res:
                return error_res
        lesson = Lesson()
        lesson.save()
        booking = Booking(
            lesson_info=lesson,
            student=Profile.objects.get(user=request.user),
            availability=Availability.objects.get(pk=availability_id),
        )
        booking.save()
        return HttpResponseRedirect(
            reverse("lessons:booking_display_student")
        )
