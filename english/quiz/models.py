from dictionary.models import Dictionary
from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Quiz(models.Model):
    student = models.ForeignKey(User,
                                verbose_name="Student",
                                on_delete=models.CASCADE,
                                related_name="quizzes")
    datetime = models.DateTimeField("Quiz time",
                                    auto_now_add=True,
                                    blank=True,
                                    null=True)

    @property
    def all_questions(self) -> list:
        return self.questions.all()

    def count_score(self) -> int:
        """Returns with number of questions with correct answers."""
        return sum(
            question.is_answer_correct for question in self.all_questions
        )

    class Meta:
        verbose_name_plural = "Quizzes"


class Question(models.Model):
    quiz = models.ForeignKey(
        Quiz, on_delete=models.CASCADE, related_name="questions"
    )
    word = models.ForeignKey(Dictionary, on_delete=models.CASCADE)
    user_answer = models.CharField(max_length=255)
    options = models.JSONField(default=list)

    @property
    def is_answer_correct(self) -> bool:
        return self.word.translation == self.user_answer
