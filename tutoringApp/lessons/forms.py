"""Forms for the lessons app."""
from django import forms

from lessons.models import Booking


class BookingForm(forms.ModelForm):
    """Form for creating Booking objects."""

    class Meta:
        model = Booking
        exclude = "__all__"
