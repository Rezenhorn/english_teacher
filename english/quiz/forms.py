from django import forms

WORDS_IN_QUIZ_CHOICES = [
    (10, "10"),
    (20, "20"),
    (30, "30"),
    (40, "40")
]
QUIZ_MODE_CHOICES = [
    ("last_lesson", "Last lesson"),
    ("all_words", "All words")
]


class SetupQuizForm(forms.Form):
    quiz_mode = forms.ChoiceField(
        choices=QUIZ_MODE_CHOICES,
        widget=forms.RadioSelect,
    )
    number_of_words = forms.ChoiceField(
        choices=WORDS_IN_QUIZ_CHOICES,
        widget=forms.RadioSelect,
    )
