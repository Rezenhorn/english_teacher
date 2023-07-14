from django.contrib import admin
from django.db import models
from django.forms import Textarea

from .models import Question, Quiz


class QuestionAdminInline(admin.TabularInline):
    model = Question
    exclude = ("user_answer",)
    raw_id_fields = ("word",)
    min_num = 2
    extra = 0
    formfield_overrides = {
        models.JSONField: {
            "widget": Textarea(attrs={"cols": "50", "rows": "1"})
        },
    }


@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ("pk", "student", "quiz_time")
    list_filter = ("student",)
    inlines = (QuestionAdminInline,)
