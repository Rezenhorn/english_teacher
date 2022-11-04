from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from .forms import DictionaryForm, HomeworkForm
from .mixins import SuperuserOrAuthorMixin, SuperuserRequiredMixin
from .models import Dictionary, Homework

User = get_user_model()


class StudentListView(LoginRequiredMixin, SuperuserRequiredMixin, ListView):
    model = User
    template_name = "students/list.html"
    context_object_name = "student_list"


class DictionaryListView(LoginRequiredMixin, SuperuserOrAuthorMixin, ListView):
    template_name = "students/dictionary.html"
    context_object_name = "dictionary"

    def get_queryset(self):
        username = self.kwargs.get("username")
        return Dictionary.objects.filter(student__username=username)

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        student = User.objects.get(username=self.kwargs.get("username"))
        data["title"] = f"{student.first_name}'s dictionary"
        data["username"] = student.username
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
        data["title"] = "Add new word"
        data["username"] = username
        return data


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
        return reverse_lazy(
            "students:student_card",
            kwargs={"username": self.kwargs.get("username")}
        )

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
        return reverse_lazy(
            "students:student_card",
            kwargs={"username": self.kwargs.get("username")}
        )


@login_required
def student_card(request, username):
    if not (request.user.is_superuser or request.user.username == username):
        return redirect("about:index")
    template = "students/student_card.html"
    student = get_object_or_404(
        User.objects.prefetch_related("homework"), username=username
    )
    if request.method == "POST":
        id_list = request.POST.getlist("boxes")
        Homework.objects.all().update(done=False)
        for id in id_list:
            Homework.objects.filter(pk=int(id)).update(done=True)
        messages.success(request, "Homeworks status has been updated")
        return redirect("students:student_card", username)
    context = {
        "student": student,
    }
    return render(request, template, context)
