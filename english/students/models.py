import datetime

import eng_to_ipa as ipa
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


class Dictionary(models.Model):
    word = models.CharField(max_length=50)
    translation = models.CharField(max_length=200)
    transcription = models.CharField(max_length=150, default="-")
    example = models.CharField(help_text="A sentence with the word",
                               max_length=150,
                               blank=True,
                               null=True)
    student = models.ForeignKey(User,
                                verbose_name="Student",
                                on_delete=models.CASCADE,
                                related_name="dictionary")
    date = models.DateField("Addition date",
                            auto_now_add=True,
                            blank=True,
                            null=True)

    class Meta:
        ordering = ("word",)
        verbose_name_plural = "Dictionaries"

    def save(self, *args, **kwargs):
        """
        Sets transcriptions for words.
        Capitalizes first letters in selected fields.
        """
        word = getattr(self, "word", False)
        if ipa.isin_cmu(word):
            if len(word.split()) == 1:
                setattr(
                    self, "transcription", " | ".join(ipa.ipa_list(word)[0])
                )
            else:
                setattr(self, "transcription", ipa.convert(word))
        for field_name in ("word", "translation"):
            value = getattr(self, field_name, False)
            if value and not value.isupper():
                setattr(self, field_name, value.capitalize())
        super(Dictionary, self).save(*args, **kwargs)

    def __str__(self):
        return self.word


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
