from django.contrib import admin

from .models import (
    Availability,
    Education,
    Language,
    Profile,
    ProfileLanguageList,
    School,
    Service,
    Subject,
)

# Register your models here.

admin.site.register(
    [
        Profile,
        Language,
        School,
        Education,
        ProfileLanguageList,
        Subject,
        Service,
        Availability,
    ]
)
