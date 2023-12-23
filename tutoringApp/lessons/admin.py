from django.contrib import admin

from .models import Booking, Entry, Lesson, Material, Solution, Task

# Register your models here.

admin.site.register([Lesson, Booking, Task, Solution, Material, Entry])
