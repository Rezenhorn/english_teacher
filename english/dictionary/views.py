from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView
from utils.decorators import author_or_superuser_required
from utils.mixins import SuperuserOrAuthorMixin

from .forms import DictionaryForm
from .models import Dictionary
from .utils import create_dictionary_xls

User = get_user_model()


class DictionaryListView(LoginRequiredMixin, SuperuserOrAuthorMixin, ListView):
    template_name = "dictionary/dictionary.html"
    context_object_name = "dictionary"
    paginate_by = settings.DICTIONARY_WORDS_PER_PAGE

    def get_queryset(self):
        queryset = Dictionary.objects.filter(
            student__username=self.kwargs.get("username")
        )
        if self.request.GET.get("o") == "date":
            queryset = queryset.order_by("-date", "word")
        query = self.request.GET.get("q")
        if query:
            queryset = queryset.filter(
                Q(word__icontains=query) | Q(translation__icontains=query)
            )
        return queryset

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        student = get_object_or_404(User, username=self.kwargs.get("username"))
        data.update(
            title=f"{student.first_name}'s dictionary",
            student=student,
            word_count=student.dictionary.count(),
            order=self.request.GET.get("o"),
            query=self.request.GET.get("q"),
        )
        return data


class DictionaryCreateView(LoginRequiredMixin,
                           SuperuserOrAuthorMixin,
                           CreateView):
    form_class = DictionaryForm
    template_name = "dictionary/dictionary_form.html"

    def form_valid(self, form):
        username = self.kwargs.get("username")
        student = get_object_or_404(User, username=username)
        dictionary = form.save(commit=False)
        dictionary.student = student
        dictionary.save()
        return redirect("dictionary:dictionary", username)

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data.update(username=self.kwargs.get("username"))
        return data


class DictionaryUpdateView(LoginRequiredMixin,
                           SuperuserOrAuthorMixin,
                           UpdateView):
    form_class = DictionaryForm
    model = Dictionary
    template_name = "dictionary/dictionary_form.html"
    pk_url_kwarg = "dictionary_id"

    def get_success_url(self):
        return reverse_lazy("dictionary:dictionary",
                            kwargs={"username": self.kwargs.get("username")})


@login_required
@author_or_superuser_required
def download_dictionary(request, username):
    """Provides download of the student's dictionary as .xls file."""
    response = HttpResponse(headers={
        "Content-Type": "application/vnd.ms-excel",
        "Content-Disposition": f"attachment; filename={username}'s_dict.xls",
    })
    create_dictionary_xls(username).save(response)
    return response
