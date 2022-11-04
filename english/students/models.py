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

    class Meta:
        ordering = ("-date",)

    def __str__(self):
        return self.description[:40]


class Dictionary(models.Model):
    word = models.CharField(max_length=50)
    translation = models.CharField(max_length=50)
    example = models.CharField(max_length=100, blank=True, null=True)
    student = models.ForeignKey(
        User,
        verbose_name="Student",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="dictionary"
    )

    class Meta:
        ordering = ("word",)
        verbose_name_plural = "Dictionaries"

    def save(self, *args, **kwargs):
        """Capitalizes first letters in selected fields."""
        for field_name in ["word", "translation", "example"]:
            val = getattr(self, field_name, False)
            if val:
                setattr(self, field_name, val.capitalize())
        super(Dictionary, self).save(*args, **kwargs)

    def __str__(self):
        return self.word
