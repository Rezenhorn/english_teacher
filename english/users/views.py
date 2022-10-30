from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView

from .forms import CreationForm


class SignUp(CreateView):
    """Регистрация пользователя."""
    form_class = CreationForm
    success_url = reverse_lazy('about:index')
    template_name = 'users/signup.html'
