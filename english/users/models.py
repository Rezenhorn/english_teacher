from datetime import date

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse

from .managers import CustomUserManager, StudentsManager


class User(AbstractUser):
    """Custom user model with student's features."""
    first_name = models.CharField("First name", max_length=150)
    last_name = models.CharField("Last name", max_length=150)
    birth_date = models.DateField("Date of birth")
    aim = models.CharField(
        verbose_name="Training objective",
        help_text="Your aim of English learning",
        max_length=100,
        blank=True
    )

    objects = CustomUserManager()
    students = StudentsManager()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def get_absolute_url(self):
        return reverse("students:student_card", args=(self.username,))

    def age(self):
        today = date.today()
        return (today.year - self.birth_date.year
                - ((today.month, today.day)
                    < (self.birth_date.month, self.birth_date.day)))
