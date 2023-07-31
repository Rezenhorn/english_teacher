import random
from typing import Iterable, Literal

from dictionary.models import Word
from django.db import transaction
from django.db.models import Count
from users.models import User

from .models import Question, Quiz


class EmptyDictionaryError(Exception):
    pass


class QuizService:
    def __init__(self, student: User) -> None:
        self.student = student

    def _get_dictionary_objects_all(
        self, questions_num: int
    ) -> Iterable[Word]:
        """Returns `questions_num` Word objects sorted randomly."""
        all_words = Word.objects.filter(student=self.student)
        number_of_words = min(int(questions_num), all_words.count())
        return random.sample(list(all_words), number_of_words)

    def _get_dictionary_objects_last_lesson(
        self, questions_num: int
    ) -> Iterable[Word]:
        """
        Returns `questions_num` Word objects with the date
        of last addition, sorted randomly.
        """
        last_lesson_words = (
            Word.objects.filter(student=self.student)
            .order_by("-date")[:1].values("date")
            .annotate(count=Count("date")).values_list("date", "count")
        )
        number_of_words = min(int(questions_num), last_lesson_words[0][1])
        return (
            Word.objects.filter(
                student=self.student, date=last_lesson_words[0][0]
            ).order_by("?")[:number_of_words]
        )

    def _create_question(self, word: Word, quiz: Quiz) -> Question:
        translations_except_current = set(
            self.student.words.values_list("translation", flat=True)
        )
        translations_except_current.discard(word.translation)
        try:
            options = random.sample(translations_except_current, k=2)
        except ValueError:
            raise EmptyDictionaryError(
                "There are too few words in the dictionary for the quiz."
            )
        options.append(word.translation)
        random.shuffle(options)
        return Question.objects.create(quiz=quiz, word=word, options=options)

    @transaction.atomic
    def create(
        self,
        *,
        mode: Literal["all_words", "last_lesson"],
        questions_num: int
    ) -> Quiz:
        modes = {
            "all_words": self._get_dictionary_objects_all,
            "last_lesson": self._get_dictionary_objects_last_lesson
        }
        try:
            words = modes[mode](questions_num)
        except IndexError:
            raise EmptyDictionaryError("Student's dictionary is empty.")
        quiz = Quiz.objects.create(student=self.student)
        for word in words:
            self._create_question(word, quiz)
        return quiz

    def delete_last(self) -> None:
        self.student.quizzes.order_by("-datetime").first().delete()

    def delete_all(self) -> None:
        self.student.quizzes.all().delete()
