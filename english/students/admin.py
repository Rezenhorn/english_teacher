from django.contrib import admin

from .models import Dictionary, Homework, Progress


@admin.register(Homework)
class HomeworkAdmin(admin.ModelAdmin):
    list_display = ("student", "description", "date", "done")
    list_filter = ("student", "done")
    search_fields = ("student", "decsription")


@admin.register(Dictionary)
class DictionaryAdmin(admin.ModelAdmin):
    list_display = ("word", "translation", "example", "student")
    list_filter = ("student",)
    search_fields = ("word", "translation", "student")


@admin.register(Progress)
class DictionaryAdmin(admin.ModelAdmin):
    list_display = ("topic", "student", "done")
    list_filter = ("student",)
    search_fields = ("topic", "student")
