from typing import Any

from django import forms
from django.contrib import admin

from lessons.models import Profile
from tutors.models import Subject

from .models import Appointment, Review, ServiceSubscriptionList, Subscription

# Register your models here.


admin.site.register([ServiceSubscriptionList, Appointment, Review])


class SubscriptionForm(forms.ModelForm):
    """Form for the Subscription class."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        try:
            self.fields["subject"].queryset = Subject.objects.filter(
                service__tutor=self.instance.tutor, service__is_default=True
            )
        except Subscription.tutor.RelatedObjectDoesNotExist:
            pass

    class Meta:
        model = Subscription
        fields = "__all__"


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ("pk", "tutor", "student", "subject")
    form = SubscriptionForm

    def get_form(self, request, obj=None, **kwargs) -> Any:
        form = super().get_form(request, obj, **kwargs)
        form.base_fields["tutor"].queryset = Profile.objects.filter(
            teaching_since__isnull=False
        )
        form.base_fields["student"].queryset = Profile.objects.filter(
            teaching_since__isnull=True
        )

        return form
