"""Views for the `create_appointment` page."""
from logging import getLogger
from typing import Optional

from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.http.request import HttpRequest
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse

from lessons.models import Lesson
from profiles.models import Profile
from subscriptions.models import Appointment, ServiceSubscriptionList, Subscription

LOGGER = getLogger(__name__)


def get_unbooked_service_subscription_list_object(
    subscription: Subscription,
) -> Optional[ServiceSubscriptionList]:
    """Get first unbooked ServiceSubscriptionList object.

    A ServiceSubscriptionList object is 'booked' if the number
    of related Appointment objects is equal to the value
    of `number_of_hours` field in the related Service object.
    The method fetches all ServiceSubscriptionList objects
    related to provided Subscription, sorts them by purchase
    date and then performs the checks of the number of
    Appointments on each of them in order. First ServiceSubscriptionList
    object that is not fully booked ends up being returned.

    Args:
        subscription: An instance of the Subscription class that the
                        soon-to-be-checked ServiceSubscriptionList
                        objects are related to.
    Returns:
        First ServiceSubscriptionList object that is not fully
        booked if such object exists, None otherwise.
    """
    service_subscription_lists = ServiceSubscriptionList.objects.filter(
        subscription=subscription,
        service__tutor=Profile.objects.get(user=subscription.tutor),
    ).order_by("purchase_date")
    for service_subscription_list in service_subscription_lists:
        appointments = service_subscription_list.appointment_set.all()
        if len(appointments) < service_subscription_list.service.number_of_hours:
            return service_subscription_list


@login_required
def create_appointment_view(request: HttpRequest, subscription_id: int) -> HttpResponse:
    """Create appointment for a given Subscription.

    The view createas an Appointment and Lesson objects
    ralated to a given Subscription. There is also a check
    made to ensure that the currently logged in user
    it the Tutor related to the Subscription. There
    are also related ServiceSubscriptionList and Appointment
    objects fetched to ensure that there are hours left
    that could be 'allocated' for the newly created Appointment.

    Args:
        request: An instance of the HttpRequest class, containing
                every information about the request sent to the server.
        subscription_id: Primary key of the Subscription object that
                            the newly created Appointment object
                            will be related to.
    Returns:
        An instance of the HttpResponse class displaying
        different pages depending on whether the Subscription
        object was found or not, the logged in user was the
        Tutor related to a given Subsctiprion object and and
        there were hours left that could be allocated for the
        new Appointment.
    """
    subscription = get_object_or_404(Subscription, pk=subscription_id)

    if request.user != subscription.tutor.user:
        return render(
            request=request,
            template_name="tutoringApp/forbidden.html",
            status=403,
            context={
                "warning_message": "As a Student you are not allowed to create Appointments."
                if Profile.objects.get(user=request.user).is_student()
                else "You are not allowed to create Appointments under Subscriptions assigned to another Tutor.",
                "redirect_link": reverse("home:home"),
                "redirect_destination": "home page",
            },
        )

    unbooked_service_subscription_list = get_unbooked_service_subscription_list_object(
        subscription
    )

    if not unbooked_service_subscription_list:
        return render(
            request=request,
            template_name="tutoringApp/forbidden.html",
            status=403,
            context={
                "warning_message": "No hours left available in the Subscription.",
                "redirect_link": reverse(
                    "subscriptions:learning_tutor",
                    kwargs={"subscription_id": subscription.pk},
                ),
                "redirect_destination": "subscription's page",
            },
        )

    if request.method == "POST":
        lesson = Lesson.objects.create()
        Appointment.objects.create(
            lesson_info=lesson,
            subscription_service=get_unbooked_service_subscription_list_object(
                subscription
            ),
        )

        return HttpResponseRedirect(
            reverse("lessons:lesson_update", kwargs={"pk": lesson.pk})
        )
    return HttpResponseRedirect(
        reverse(
            "subscriptions:learning_tutor",
            kwargs={"subscription_id": subscription.pk},
        )
    )
