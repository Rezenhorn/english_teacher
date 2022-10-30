from django.contrib import admin

from .models import User


@admin.register(User)
class PostAdmin(admin.ModelAdmin):
    list_display = ('username', 'first_name', 'last_name')
    search_fields = ('first_name',)
