from django.contrib import admin

from .models import Word


@admin.register(Word)
class WordAdmin(admin.ModelAdmin):
    list_display = (
        "word", "translation", "transcription", "example", "student", "date"
    )
    list_filter = ("student",)
    search_fields = ("word", "translation")
