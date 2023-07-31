from dictionary.models import Word
from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Quiz(models.Model):
    student = models.ForeignKey(User,
                                verbose_name="Student",
                                on_delete=models.CASCADE,
                                related_name="quizzes")
    quiz_time = models.DateTimeField("Quiz time",
                                     auto_now_add=True,
                                     blank=True,
                                     null=True)

    @property
    def all_questions(self) -> models.query.QuerySet:
        return self.questions.select_related("word")

    def count_score(self) -> int:
        """Returns with number of questions with correct answers."""
        return sum(
            question.is_answer_correct for question in self.all_questions
        )

    class Meta:
        verbose_name_plural = "Quizzes"

    def __str__(self):
        return f"Quiz #{self.id} - {self.student.username}"


class Question(models.Model):
    quiz = models.ForeignKey(
        Quiz, on_delete=models.CASCADE, related_name="questions"
    )
    word = models.ForeignKey(
        Word, on_delete=models.CASCADE, related_name="+"
    )
    user_answer = models.CharField(
        "Answer of student", max_length=255, blank=True
    )
    options = models.JSONField(
        "Answer options",
        default=list,
        help_text='Example: ["option1", "option2", "option3"]'
    )

    @property
    def is_answer_correct(self) -> bool:
        return self.word.translation == self.user_answer

    def __str__(self):
        return f"Question<{self.word.word}: {self.word.translation}>"
