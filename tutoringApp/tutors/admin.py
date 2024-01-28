"""Module for configuring the admin site."""
from django.contrib import admin

from tutors.models import Availability, Service, Subject

# Register your models here.

admin.site.register([Subject, Availability])

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ("pk", "subject", "tutor", "number_of_hours")
