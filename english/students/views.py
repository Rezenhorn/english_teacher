from django.conf import settings
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView
from utils.decorators import author_or_superuser_required
from utils.messages import HOMEWORK_UPDATED_MESSAGE
from utils.mixins import SuperuserOrAuthorMixin, SuperuserRequiredMixin

from .forms import HomeworkForm
from .models import Homework, Progress

User = get_user_model()


class StudentListView(LoginRequiredMixin, SuperuserRequiredMixin, ListView):
    template_name = "students/list.html"
    context_object_name = "student_list"

    def get_queryset(self):
        return {"active": User.students.filter(is_active=True),
                "inactive": User.students.filter(is_active=False)}


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
        data.update(
            title=f"New homework for {student}",
            username=username
        )
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
        data.update(title=f"Edit homework for {self.kwargs.get('username')}")
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
        student = get_object_or_404(User, username=self.kwargs.get("username"))
        data.update(student=student)
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
        messages.success(request, HOMEWORK_UPDATED_MESSAGE)
        return redirect("students:student_card", username)
    context = {
        "page_obj": paginator(request.GET.get("page"), homework),
        "student": student,
    }
    return render(request, template, context)
