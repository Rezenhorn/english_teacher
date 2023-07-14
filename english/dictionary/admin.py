from django.contrib import admin

from .models import Dictionary


@admin.register(Dictionary)
class DictionaryAdmin(admin.ModelAdmin):
    list_display = (
        "word", "translation", "transcription", "example", "student", "date"
    )
    list_filter = ("student",)
    search_fields = ("word", "translation")
