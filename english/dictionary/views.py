from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView
from utils.decorators import author_or_superuser_required
from utils.mixins import SuperuserOrAuthorMixin

from .forms import WordForm
from .models import Word
from .selectors import get_words
from .services import create_dictionary_xls

User = get_user_model()


class WordListView(LoginRequiredMixin, SuperuserOrAuthorMixin, ListView):
    template_name = "dictionary/dictionary.html"
    context_object_name = "dictionary"
    paginate_by = settings.DICTIONARY_WORDS_PER_PAGE

    def get_queryset(self):
        self.student = User.objects.get(username=self.kwargs.get("username"))
        search_query = self.request.GET.get("q")
        ordering = self.request.GET.get("o")
        return get_words(
            student=self.student,
            search_query=search_query,
            ordering=ordering
        )

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data.update(
            title=f"{self.student.first_name}'s dictionary",
            student=self.student,
            word_count=len(self.object_list),
            order=self.request.GET.get("o"),
            query=self.request.GET.get("q"),
        )
        return data


class WordCreateView(LoginRequiredMixin, SuperuserOrAuthorMixin, CreateView):
    form_class = WordForm
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


class WordUpdateView(LoginRequiredMixin, SuperuserOrAuthorMixin, UpdateView):
    form_class = WordForm
    model = Word
    template_name = "dictionary/dictionary_form.html"
    pk_url_kwarg = "word_id"

    def get_success_url(self):
        return reverse_lazy("dictionary:dictionary",
                            kwargs={"username": self.kwargs.get("username")})

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data.update(
            username=self.kwargs.get("username"),
        )
        return data


class WordDeleteView(LoginRequiredMixin, SuperuserOrAuthorMixin, DeleteView):
    model = Word
    pk_url_kwarg = "word_id"

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

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
