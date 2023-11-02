from django.http import HttpResponse, HttpRequest
from django.shortcuts import render

def homeView(request: HttpRequest) -> HttpResponse:
    """Displays a bacis homepage."""
    return render(request, 'home/home.html')