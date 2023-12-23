"""Views for managin Booking objects."""
from logging import getLogger

from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from lessons.models import Booking, Lesson
from profiles.models import Profile
from tutors.models import Availability

LOGGER = getLogger(__name__)


@login_required
def create_booking_view(request: HttpRequest, availability_id: int) -> HttpResponse:
    """Create Booking and corresponding Lesson object.

    The view checks if the request sent is a POST or GET request.
    In case of POST, new Booking and Lesson objects are created.
    In case of GET there is a check made to ensure the requestor
    is a Student and if so, a confirmation page is rendered. In
    other case, the requesting Tutor is warned and redirected to
    the home page. The view also checks if the related Availavility
    object does exist. If not, a page with a warning message is displayed.

    Args:
        request: An instance of the HttpRequest class, containing
                every information about the request sent to the server.
        availability_id: Primary key of the Availability object that the
                Booking will be related to.

    Returns:
        Instance of the HttpResponse class, redirecting Students to their
        profile after successful booking or Tutors to a page with a warning
        message in case of POST request. In case of GET, a booking confirmation
        page is displayed if the related Availability object does exist. In other case,
        a page with a warning message is displayed.
    """
    if request.method == "GET":
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
        lesson = Lesson()
        lesson.save()
        booking = Booking(
            lesson_info=lesson,
            student=Profile.objects.get(user=request.user),
            availability=Availability.objects.get(pk=availability_id),
        )
        booking.save()
        return HttpResponseRedirect(
            reverse("profiles:student_display", kwargs={"pk": request.user.pk})
        )
