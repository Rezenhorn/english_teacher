import datetime
from django import forms
from django.contrib.auth import get_user_model

from .models import Dictionary, Homework


User = get_user_model()


class HomeworkForm(forms.ModelForm):
    class Meta:
        year_now = datetime.date.today().year
        model = Homework
        fields = ('description', 'date')
        widgets = {
            'description': forms.Textarea(attrs={
                'placeholder': 'Enter the homework text',
                'rows': 3,
            }),
            'date': forms.SelectDateWidget(years=range(year_now, year_now + 2))
        }


class DictionaryForm(forms.ModelForm):
    class Meta:
        model = Dictionary
        fields = ('word', 'translation', 'example')
