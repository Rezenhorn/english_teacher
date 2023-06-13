from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView
from utils.mixins import SuperuserOrAuthorMixin

from .forms import CreationForm, UserEditForm

User = get_user_model()


class SignUp(CreateView):
    """User sign up."""
    form_class = CreationForm
    success_url = reverse_lazy("about:index")
    template_name = "users/signup.html"


class UserEditView(LoginRequiredMixin,
                   SuperuserOrAuthorMixin,
                   UpdateView):
    """Profile info edit view."""
    queryset = User.objects.all()
    form_class = UserEditForm
    success_url = reverse_lazy("about:index")
    template_name = "users/edit_profile.html"
    pk_url_kwarg = "user_id"
