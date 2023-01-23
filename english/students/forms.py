import datetime

from bootstrap_datepicker_plus.widgets import DatePickerInput
from django import forms
from django.conf import settings
from django.contrib.auth import get_user_model
from django.forms import ValidationError
from django.utils import timezone

from .models import Dictionary, Homework

User = get_user_model()


class HomeworkForm(forms.ModelForm):
    def clean_date(self):
        """Ensures that the date is not in the past."""
        date = self.cleaned_data["date"]
        if date < timezone.now().date():
            raise ValidationError(f"Wrong date: {date}. "
                                  "Try to choose the date in future")
        return date

    class Meta:
        year_now = datetime.date.today().year
        model = Homework
        fields = ("description", "date")
        widgets = {
            "description": forms.Textarea(attrs={
                "placeholder": "Enter the homework text",
                "rows": 3,
            }),
            "date": DatePickerInput(
                options={"format": settings.DATE_INPUT_FORMATS}
            )
        }


class DictionaryForm(forms.ModelForm):
    class Meta:
        model = Dictionary
        fields = ("word", "translation", "example")
