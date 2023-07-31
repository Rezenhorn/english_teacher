import eng_to_ipa as ipa
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
        super(Word, self).save(*args, **kwargs)

    def __str__(self):
        return self.word
