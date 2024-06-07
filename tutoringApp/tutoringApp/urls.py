"""URL configuration for tutoringApp project."""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("home.urls")),
    path("profiles/", include("profiles.urls")),
    path("tutors/", include("tutors.urls")),
    path("lessons/", include("lessons.urls")),
    path("subscriptions/", include("subscriptions.urls")),
    path("search/", include("search.urls")),
    path("chat/", include("chat.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
