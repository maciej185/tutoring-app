"""Forms for the `tutors` app."""
from django import forms

from profiles.models import Profile
from tutors.models import Service, Subject


class ServiceForm(forms.ModelForm):
    """Form for inputting info about services offered by a given Tutor."""

    class Meta:
        model = Service
        exclude = ["tutor", "is_default"]

        SESSION_LENGTH_CHOICES = [
            (length, str(length)) for length in range(30, 181, 15)
        ]

        widgets = {
            "subject": forms.Select(attrs={"class": "options"}),
            "price_per_hour": forms.NumberInput(attrs={"class": "number-input"}),
            "number_of_hours": forms.NumberInput(attrs={"class": "number-input"}),
            "session_length": forms.Select(
                attrs={"class": "options"}, choices=SESSION_LENGTH_CHOICES
            ),
        }


class ServiceInlineFormset(forms.BaseInlineFormSet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            for form in self.forms:
                form.fields["subject"].queryset = (
                    Subject.objects.filter(service__tutor=self.instance.pk)
                    .filter(service__is_default=True)
                    .filter(service__number_of_hours=1)
                    .distinct()
                )


service_formset = forms.inlineformset_factory(
    parent_model=Profile,
    model=Service,
    form=ServiceForm,
    formset=ServiceInlineFormset,
    extra=1,
    can_delete=True,
    can_delete_extra=False,
    min_num=0,
)
