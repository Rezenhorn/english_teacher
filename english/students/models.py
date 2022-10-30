from django.contrib.auth import get_user_model
from django.db import models


User = get_user_model()


class Homework(models.Model):
    description = models.TextField(verbose_name="Task")
    date = models.DateField(verbose_name="Date of homework")
    student = models.ForeignKey(
        User,
        verbose_name="Student",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="homework"
    )
    done = models.BooleanField(verbose_name="Done", default=False)

    def __str__(self):
        return self.description[:40]
