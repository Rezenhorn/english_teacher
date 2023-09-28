from typing import Any, Iterable

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.cache import cache
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView
from utils.decorators import author_or_superuser_required
from utils.json_helpers import deserialize_queryset, serialize_queryset
from utils.mixins import SuperuserOrAuthorMixin

from .forms import WordForm
from .models import Word
from .services import create_dictionary_xls

User = get_user_model()


class WordListView(LoginRequiredMixin, SuperuserOrAuthorMixin, ListView):
    template_name = "dictionary/dictionary.html"
    context_object_name = "dictionary"
    paginate_by = settings.DICTIONARY_WORDS_PER_PAGE

    @staticmethod  # TODO: посмотреть по DDD
    def search_words(search_query: str, queryset: Iterable[Word]):
        result = queryset
        if len(search_query) > 2:
            result = filter(
                lambda word: search_query.lower() in word.translation.lower()
                or search_query.lower() in word.word.lower(),
                queryset
            )
        return result

    @staticmethod
    def order_words(ordering: str, queryset: Iterable[Word]) -> list[Word]:
        match ordering:
            case "date":
                return sorted(
                    queryset, key=lambda word: word.date, reverse=True
                )
            case "translation":
                return sorted(
                    queryset,
                    key=lambda word: word.translation.lower()
                )
        return queryset

    def get_queryset(self):
        self.student: User = User.objects.get(
            username=self.kwargs.get("username")
        )
        search_query = self.request.GET.get("query")
        ordering = self.request.GET.get("ordering")
        cache_key: str = f"dict_{self.student.id}"
        dictionary = cache.get(cache_key)
        if not dictionary:
            dictionary = serialize_queryset(self.student.words.all())
            cache.set(cache_key, dictionary, settings.CACHE_TTL_FOR_DICTIONARY)
        result = deserialize_queryset(dictionary)
        if search_query:
            result = self.search_words(search_query, result)
        if ordering:
            result = self.order_words(ordering, result)
        return list(result)

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        data = super().get_context_data(**kwargs)
        data.update(
            title=f"{self.student.first_name}'s dictionary",
            student=self.student,
            word_count=len(self.object_list),
            order=self.request.GET.get("ordering"),
            query=self.request.GET.get("query"),
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

    def get_context_data(self, **kwargs) -> dict[str, Any]:
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

    def get_context_data(self, **kwargs) -> dict[str, Any]:
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
def download_dictionary(request: HttpRequest, username: str) -> HttpResponse:
    """Provides download of the student's dictionary as .xls file."""
    response = HttpResponse(headers={
        "Content-Type": "application/vnd.ms-excel",
        "Content-Disposition": f"attachment; filename={username}'s_dict.xls",
    })
    create_dictionary_xls(username).save(response)
    return response
