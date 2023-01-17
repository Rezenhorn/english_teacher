from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserChangeForm, UserCreationForm

User = get_user_model()


class CreationForm(UserCreationForm):
    """Форма создания пользователя."""

    class Meta(UserCreationForm.Meta):
        model = User
        fields = (
            "first_name", "last_name", "username", "email", "birth_date", "aim"
        )
        widgets = {
            "birth_date": forms.SelectDateWidget(years=range(1950, 2014))
        }


class UserEditForm(UserChangeForm):
    """User profile edit form."""

    class Meta(UserChangeForm.Meta):
        model = User
        fields = (
            "first_name", "last_name", "username", "email", "birth_date", "aim"
        )
        widgets = {
            "birth_date": forms.SelectDateWidget(years=range(1950, 2014))
        }
