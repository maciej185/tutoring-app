"""Forms for the lessons app."""
from django import forms

from lessons.models import Booking, Lesson, Material, Task


class LessonForm(forms.ModelForm):
    """Form for updating Lesson objects."""

    class Meta:
        model = Lesson
        exclude = ["status"]

        widgets = {
            "date": forms.DateTimeInput(
                attrs={"type": "datetime-local"},
            )
        }


class BookingForm(forms.ModelForm):
    """Form for creating Booking objects."""

    class Meta:
        model = Booking
        exclude = "__all__"


class TaskForm(forms.ModelForm):
    """Form for creating Task objects."""

    class Meta:
        model = Task
        exclude = ["lesson", "status"]


task_formset = forms.inlineformset_factory(
    parent_model=Lesson,
    model=Task,
    form=TaskForm,
    extra=1,
    can_delete=True,
    can_delete_extra=False,
    min_num=0,
)


class MaterialForm(forms.ModelForm):
    """Form for creating Material objects."""

    class Meta:
        model = Material
        exclude = ["lesson", "upload_date"]


material_formset = forms.inlineformset_factory(
    parent_model=Lesson,
    model=Material,
    form=MaterialForm,
    extra=1,
    can_delete=True,
    can_delete_extra=False,
    min_num=0,
)
