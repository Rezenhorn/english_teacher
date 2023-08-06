from django.contrib import admin

from .models import Homework, Progress


@admin.register(Homework)
class HomeworkAdmin(admin.ModelAdmin):
    list_display = ("student", "description", "date", "done")
    list_filter = ("student", "done")
    search_fields = ("student", "decsription")


@admin.register(Progress)
class DictionaryAdmin(admin.ModelAdmin):
    list_display = ("topic", "student", "done")
    list_editable = ("done",)
    list_filter = ("student",)
    search_fields = ("topic", "student")
