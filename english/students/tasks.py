from django.shortcuts import get_object_or_404

from english.celery import app

from .models import Homework


@app.task
def homework_toggle_done_task(homework_id: str | int) -> None:
    """Changes the boolean field `done` to the opposite value."""
    homework = get_object_or_404(Homework, id=homework_id)
    homework.done = not homework.done
    homework.save()
