from django.core.cache import cache
from django.db.models.signals import post_delete, post_save, pre_save
from django.dispatch import receiver

from .models import Word
from .tasks import get_transcription_task


@receiver(pre_save, sender=Word)
def add_transcription(sender, instance: Word, **kwargs):
    """Generates and adds transcription before saving Word instance."""
    transcription_task = get_transcription_task.delay(instance.word)
    instance.transcription = transcription_task.wait(
        timeout=None, interval=0.1
    )


@receiver([post_save, post_delete], sender=Word)
def clear_words_cache(sender, instance: Word, **kwargs):
    """Deletes all student's words from cache."""
    cache.delete_pattern(f"dict_{instance.student.pk}*")
