from django.core.cache import cache
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from .models import Homework


@receiver([post_save, post_delete], sender=Homework)
def clear_homework_cache(sender, instance: Homework, **kwargs):
    """Deletes all student's homework from cache."""
    cache.delete_pattern(f"hw_{instance.student.pk}*")
