from django.shortcuts import get_object_or_404

from .models import Homework


def homework_toggle_done(homework_id: str | int) -> None:
    """Changes the boolean field `done` to the opposite value."""
    homework = get_object_or_404(Homework, id=homework_id)
    homework.done = not homework.done
    homework.save()
