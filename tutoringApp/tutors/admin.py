"""Module for configuring the admin site."""
from django.contrib import admin

from tutors.models import Availability, Service, Subject

# Register your models here.

admin.site.register([Service, Subject, Availability])
