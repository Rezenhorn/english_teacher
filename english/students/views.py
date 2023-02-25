from django.conf import settings
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from .forms import DictionaryForm, HomeworkForm
from .mixins import SuperuserOrAuthorMixin, SuperuserRequiredMixin
from .models import Dictionary, Homework, Progress
from .utils import author_or_superuser_required, create_dictionary_xls

User = get_user_model()


class StudentListView(LoginRequiredMixin, SuperuserRequiredMixin, ListView):
    template_name = "students/list.html"
    context_object_name = "student_list"

    def get_queryset(self):
        return {"active": User.students.filter(is_active=True),
                "inactive": User.students.filter(is_active=False)}


class DictionaryListView(LoginRequiredMixin, SuperuserOrAuthorMixin, ListView):
    template_name = "students/dictionary.html"
    context_object_name = "dictionary"
    paginate_by = settings.DICTIONARY_WORDS_PER_PAGE

    def get_queryset(self):
        username = self.kwargs.get("username")
        query = self.request.GET.get("q")
        order = self.request.GET.get("o")
        queryset = Dictionary.objects.filter(student__username=username)
        if order == "date":
            queryset = queryset.order_by("-date", "word")
        if query:
            return queryset.filter(
                Q(word__icontains=query) | Q(translation__icontains=query)
            )
        return queryset

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        student = get_object_or_404(User, username=self.kwargs.get("username"))
        data["title"] = f"{student.first_name}'s dictionary"
        data["student"] = student
        data["word_count"] = student.dictionary.count()
        data["order"] = self.request.GET.get("o")
        return data


class DictionaryCreateView(LoginRequiredMixin,
                           SuperuserOrAuthorMixin,
                           CreateView):
    form_class = DictionaryForm
    template_name = "students/dictionary_form.html"

    def form_valid(self, form):
        username = self.kwargs.get("username")
        student = get_object_or_404(User, username=username)
        dictionary = form.save(commit=False)
        dictionary.student = student
        dictionary.save()
        return redirect("students:dictionary", username)

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        username = self.kwargs.get("username")
        data["username"] = username
        return data


class DictionaryUpdateView(LoginRequiredMixin,
                           SuperuserOrAuthorMixin,
                           UpdateView):
    form_class = DictionaryForm
    model = Dictionary
    template_name = "students/dictionary_form.html"
    pk_url_kwarg = "dictionary_id"

    def get_success_url(self):
        return reverse_lazy("students:dictionary",
                            kwargs={"username": self.kwargs.get("username")})


class HomeworkCreateView(LoginRequiredMixin,
                         SuperuserRequiredMixin,
                         CreateView):
    form_class = HomeworkForm
    template_name = "students/homework_form.html"

    def form_valid(self, form):
        username = self.kwargs.get("username")
        student = get_object_or_404(User, username=username)
        homework = form.save(commit=False)
        homework.student = student
        homework.save()
        return redirect("students:student_card", username)

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        username = self.kwargs.get("username")
        student = get_object_or_404(User, username=username)
        data["title"] = f"New homework for {student}"
        data["username"] = username
        return data


class HomeworkUpdateView(LoginRequiredMixin,
                         SuperuserRequiredMixin,
                         UpdateView):
    form_class = HomeworkForm
    model = Homework
    template_name = "students/homework_form.html"
    pk_url_kwarg = "homework_id"

    def get_success_url(self):
        return reverse_lazy("students:student_card",
                            kwargs={"username": self.kwargs.get("username")})

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        username = self.kwargs.get("username")
        data["title"] = f"Edit homework for {username}"
        return data


class HomeworkDeleteView(LoginRequiredMixin,
                         SuperuserRequiredMixin,
                         DeleteView):
    model = Homework
    template_name = "students/confirm_delete.html"
    pk_url_kwarg = "homework_id"

    def get_success_url(self):
        return reverse_lazy("students:student_card",
                            kwargs={"username": self.kwargs.get("username")})


class ProgressListView(LoginRequiredMixin, SuperuserOrAuthorMixin, ListView):
    template_name = "students/progress.html"
    context_object_name = "progress"
    paginate_by = settings.PROGRESS_PER_PAGE

    def get_queryset(self):
        username = self.kwargs.get("username")
        return Progress.objects.filter(student__username=username)

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        username = self.kwargs.get("username")
        student = get_object_or_404(User, username=username)
        data["student"] = student
        return data


def paginator(page_number, posts):
    """Paginator for function based views."""
    paginator = Paginator(posts, settings.HOMEWORK_PER_PAGE)
    return paginator.get_page(page_number)


@login_required
@author_or_superuser_required
def student_card(request, username):
    template = "students/student_card.html"
    student = get_object_or_404(User, username=username)
    homework = student.homework.all()
    if request.method == "POST":
        id_list = request.POST.getlist("boxes")
        homework.update(done=False)
        for id in id_list:
            homework.filter(pk=int(id)).update(done=True)
        messages.success(request, "Homeworks status has been updated")
        return redirect("students:student_card", username)
    context = {
        "page_obj": paginator(request.GET.get("page"), homework),
        "student": student,
    }
    return render(request, template, context)


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
