from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404, redirect, render


User = get_user_model()


@login_required
def student_list(request):
    if not request.user.is_superuser:
        return redirect('about:index')
    template = 'students/list.html'
    students = User.objects.all()
    context = {
        'student_list': students
    }
    return render(request, template, context)


@login_required
def student_card(request, user_id):
    if not (request.user.is_superuser or request.user.pk == user_id):
        return redirect('about:index')
    template = 'students/student_card.html'
    student = get_object_or_404(User, pk=user_id)
    context = {
        'student': student
    }
    return render(request, template, context)
