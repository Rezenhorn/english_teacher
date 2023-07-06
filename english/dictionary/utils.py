import random
from typing import Iterable, List

import xlwt
from django.contrib.auth import get_user_model
from django.db.models import Count
from django.shortcuts import get_object_or_404
from typing_extensions import Literal

from .models import Dictionary

User = get_user_model()


class EmptyDictionaryError(Exception):
    pass


def create_dictionary_xls(username: str) -> xlwt.Workbook:
    """Return the excel workbook with student's dictionary."""
    workbook = xlwt.Workbook(encoding="utf-8")
    worksheet = workbook.add_sheet("Dictionary")
    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True
    columns = ["Word", "Transcription", "Translation", "Example"]

    for col_num in range(len(columns)):
        worksheet.write(row_num, col_num, columns[col_num], font_style)

    font_style = xlwt.XFStyle()
    user = get_object_or_404(User, username=username)
    rows = user.dictionary.values_list(
        "word", "transcription", "translation", "example"
    )

    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            worksheet.write(row_num, col_num, str(row[col_num]), font_style)
    return workbook


class Quiz:
    """Class for dictionary quizzes."""

    def __init__(self, username: str) -> None:
        self.username = username
        self.questions: List[dict] = []

    def _get_dictionary_objects_all(
        self, questions_num: int
    ) -> Iterable[Dictionary]:
        """Returns `questions_num` Dictionary objects sorted randomly."""
        all_words = Dictionary.objects.filter(student__username=self.username)
        number_of_words = min(int(questions_num), all_words.count())
        return random.sample(list(all_words), number_of_words)

    def _get_dictionary_objects_last_lesson(
        self, questions_num: int
    ) -> Iterable[Dictionary]:
        """
        Returns `questions_num` Dictionary objects with the date
        of last addition, sorted randomly.
        """
        last_lesson_words = (
            Dictionary.objects.filter(student__username=self.username)
            .order_by("-date")[:1].values("date")
            .annotate(count=Count("date")).values_list("date", "count")
        )
        number_of_words = min(int(questions_num), last_lesson_words[0][1])
        return (
            Dictionary.objects.filter(
                student__username=self.username, date=last_lesson_words[0][0]
            ).order_by("?")[:number_of_words]
        )

    def generate_questions(
        self,
        mode: Literal["all_words", "last_lesson"],
        questions_num: int
    ) -> None:
        """
        Populates `self.questions` with `questions_num` questions
        with Dictionary words and translations.
        Has two modes:
        - `all_words` - chooses words from whole student's dictionary
        - `last_lesson` - chooses words with the date of last addition
        """
        modes = {
            "all_words": self._get_dictionary_objects_all,
            "last_lesson": self._get_dictionary_objects_last_lesson
        }
        try:
            words = modes[mode](questions_num)
        except IndexError:
            raise EmptyDictionaryError("Student's dictionary is empty.")
        for word in words:
            translations_except_current = set(
                Dictionary.objects.values_list("translation", flat=True)
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

            self.questions.append({
                "word": word.word,
                "options": options,
                "correct_answer": word.translation
            })

    def count_correct_answers(self) -> int:
        """Returns the number of correct answers in the quiz."""
        return sum(
            question["user_answer"] == question["correct_answer"]
            for question in self.questions
        )
