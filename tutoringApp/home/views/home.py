from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from profiles.forms import AccountType


def homeView(request: HttpRequest) -> HttpResponse:
    """Displays a basic homepage."""
    account_type = request.session.get("account_type")
    if account_type:
        return (
            render(request, "home/home_student.html")
            if account_type == AccountType.STUDENT.value
            else render(request, "home/home_tutor.html")
        )
    return render(request, "home/home.html")
