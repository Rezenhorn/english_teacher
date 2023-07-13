from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import FormView
from utils.decorators import author_or_superuser_required
from utils.mixins import SuperuserOrAuthorMixin

from .forms import SetupQuizForm
from .models import Quiz
from .services import EmptyDictionaryError, QuizService

User = get_user_model()


class SetupQuizFormView(LoginRequiredMixin,
                        SuperuserOrAuthorMixin,
                        FormView):
    template_name = "quiz/quiz_setup.html"
    form_class = SetupQuizForm

    def form_valid(self, form):
        """If the form is valid, redirect to the supplied URL."""
        quiz_mode = form.cleaned_data["quiz_mode"]
        number_of_words = int(form.cleaned_data["number_of_words"])
        student = get_object_or_404(User, username=self.kwargs.get("username"))
        quiz_service = QuizService(student=student)
        try:
            quiz_service.delete_all()
            quiz = quiz_service.create(
                mode=quiz_mode,
                questions_num=number_of_words
            )
        except EmptyDictionaryError:
            messages.info(
                self.request,
                "Please, add a few words "
                "to your dictionary before taking the quiz"
            )
            return redirect(
                "dictionary:dictionary", self.kwargs.get("username")
            )
        return HttpResponseRedirect(self.get_success_url(quiz.pk))

    def get_success_url(self, quiz_id: int):
        """Return the URL to redirect to after processing a valid form."""
        return reverse_lazy(
            "quiz:quiz",
            kwargs={
                "username": self.kwargs.get("username"),
                "quiz_id": quiz_id
            }
        )

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data.update(username=self.kwargs.get("username"))
        return data


@login_required
@author_or_superuser_required
def quiz_view(request, username, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    quiz_questions = quiz.all_questions
    context = {
        "questions": quiz_questions,
        "quiz_pk": quiz.pk,
        "username": username
    }
    if request.method == "POST":
        for question in quiz_questions:
            question.user_answer = request.POST.get(question.word.word)
            question.save()
        score = quiz.count_score()
        context.update(
            score=score,
            result_percentage=int(score / len(quiz_questions) * 100)
        )
        return render(request, "quiz/quiz_result.html", context)
    return render(request, "quiz/quiz.html", context)
