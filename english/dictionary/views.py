from django.conf import settings
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, FormView, ListView, UpdateView
from utils.decorators import author_or_superuser_required
from utils.mixins import SuperuserOrAuthorMixin

from .forms import DictionaryForm, SetupQuizForm
from .models import Dictionary
from .utils import EmptyDictionaryError, Quiz, create_dictionary_xls

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


class SetupQuizFormView(LoginRequiredMixin,
                        SuperuserOrAuthorMixin,
                        FormView):
    template_name = "dictionary/quiz_setup.html"
    form_class = SetupQuizForm

    def form_valid(self, form):
        """If the form is valid, redirect to the supplied URL."""
        quiz_mode = form.cleaned_data["quiz_mode"]
        number_of_words = int(form.cleaned_data["number_of_words"])
        return HttpResponseRedirect(
            self.get_success_url(quiz_mode, number_of_words)
        )

    def get_success_url(self, quiz_mode: str, number_of_words: int):
        """Return the URL to redirect to after processing a valid form."""
        return reverse_lazy(
            "dictionary:quiz",
            kwargs={
                "username": self.kwargs.get("username"),
                "mode": quiz_mode,
                "number_of_words": number_of_words
            }
        )

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data.update(username=self.kwargs.get("username"))
        return data


@login_required
@author_or_superuser_required
def quiz_view(request, username, mode, number_of_words):
    if request.method == "POST":
        questions = request.session.get("questions")
        if questions is None:
            messages.info(request, message="Please, set up the new quiz")
            return redirect("dictionary:setup_quiz", username)
        quiz = Quiz(username)
        questions = [
            {**question, "user_answer": request.POST.get(question["word"])}
            for question in questions
        ]
        quiz.questions = questions
        score = quiz.count_correct_answers()
        request.session["result_percentage"] = int(
            score / number_of_words * 100
        )
        request.session["questions"] = questions
        return redirect(
            "dictionary:quiz_result",
            score=score,
            username=username
        )
    quiz = Quiz(username)
    try:
        quiz.generate_questions(mode, number_of_words)
    except EmptyDictionaryError:
        messages.info(
            request,
            "Please, add a few words to your dictionary before taking the quiz"
        )
        return redirect("dictionary:dictionary", username)
    questions = quiz.questions
    request.session["questions"] = questions
    context = {
        "questions": questions,
        "username": username,
        "mode": mode,
        "number_of_words": len(questions)
    }
    return render(request, "dictionary/quiz.html", context)


@login_required
@author_or_superuser_required
def quiz_result_view(request, username, score):
    questions = request.session.get("questions")
    if questions is None:
        messages.info(request, message="Please, set up the new quiz")
        return redirect("dictionary:setup_quiz", username)
    result_percentage = request.session.get("result_percentage")
    del request.session["questions"]
    del request.session["result_percentage"]
    context = {
        "username": username,
        "score": score,
        "questions": questions,
        "result_percentage": result_percentage
    }
    return render(request, "dictionary/quiz_result.html", context)
