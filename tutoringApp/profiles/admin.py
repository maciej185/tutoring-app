from django.contrib import admin
from .models import Profile, Language, School, Education, ProfileLanguageList
# Register your models here.

admin.site.register([Profile, Language, School, Education, ProfileLanguageList])
