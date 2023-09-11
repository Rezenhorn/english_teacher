from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Word(models.Model):
    word = models.CharField(max_length=50)
    translation = models.CharField(max_length=200)
    transcription = models.CharField(max_length=150, default="-")
    example = models.CharField(help_text="A sentence with the word",
                               max_length=150,
                               default="-")
    student = models.ForeignKey(User,
                                verbose_name="Student",
                                on_delete=models.CASCADE,
                                related_name="words")
    date = models.DateField("Addition date",
                            auto_now_add=True,
                            blank=True,
                            null=True)

    class Meta:
        ordering = ("word",)

    def __str__(self):
        return self.word
