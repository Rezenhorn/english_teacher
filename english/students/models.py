import datetime

from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Homework(models.Model):
    description = models.TextField(verbose_name="Task")
    date = models.DateField(verbose_name="Date of homework",
                            default=datetime.date.today)
    student = models.ForeignKey(
        User,
        verbose_name="Student",
        on_delete=models.CASCADE,
        related_name="homework"
    )
    done = models.BooleanField(verbose_name="Done", default=False)

    class Meta:
        ordering = ("-date",)

    def __str__(self):
        return f"For {self.student}: {self.description[:40]}"


class Progress(models.Model):
    topic = models.CharField(max_length=100)
    student = models.ForeignKey(User,
                                verbose_name="Student",
                                on_delete=models.CASCADE,
                                related_name="progress")
    done = models.BooleanField(verbose_name="Done", default=False)

    class Meta:
        verbose_name_plural = "Progress"
        ordering = ("id",)

    def __str__(self):
        return f"{self.topic}: {self.student}"
