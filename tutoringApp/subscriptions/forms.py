"""Forms for the `subscription` app."""
from django import forms
from subscriptions.models import Subscription
from tutors.models import Subject
from profiles.models import Profile

class SubscriptionForm(forms.ModelForm):
    """Form for the Subscritpion class."""

    def __init__(self, *args, **kwargs) -> None:
        """Limit available choices for `subject` and `student` fields.
        
        The method limits the choices for the `subject` field
        only to Subjects taught by the Tutor (Subjects that 
        are related to Service objects which they themselves 
        are related to a Profile instance representing the current 
        Tutor. The Service must have the `is_default` field set to True
        as well). Chocies for the `student` field are limited only to 
        Profile objects representing Students that had booked at least one
        Lesson with the given Tutor.  
        """
        super().__init__(*args, **kwargs)
        self.fields["subject"].queryset = Subject.objects.filter(
            service__tutor=self.initial["tutor"], service__is_default=True
        )
        self.fields["student"].queryset = Profile.objects.filter(booking__availability__service__tutor=self.initial["tutor"]).distinct()

    class Meta:
        model = Subscription
        fields = ["student", "subject"]