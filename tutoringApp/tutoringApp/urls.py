"""URL configuration for tutoringApp project."""

from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("home.urls")),
    path("profiles/", include("profiles.urls")),
]
