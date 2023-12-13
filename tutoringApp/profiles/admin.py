from django.contrib import admin

from .models import Education, Language, Profile, ProfileLanguageList, School

# Register your models here.

admin.site.register(
    [
        Profile,
        Language,
        School,
        Education,
        ProfileLanguageList,
    ]
)
