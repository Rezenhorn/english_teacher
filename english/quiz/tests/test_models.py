from dictionary.models import Dictionary
from django.contrib.auth import get_user_model
from django.test import TestCase

from ..models import Question, Quiz

User = get_user_model()


class QuizModelTest(TestCase):
    """Model tests of application Quiz."""
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.student = User.objects.create_user(username="student",
                                               birth_date="2000-01-01")
        cls.dictionary = Dictionary.objects.create(
            word="Test",
            translation="Тест",
            student=cls.student
        )
        for num in range(2):
            Dictionary.objects.create(
                word=f"Test{num}",
                translation=f"Тест{num}",
                student=cls.student
            )
        cls.quiz = Quiz.objects.create(student=cls.student)
        cls.question_with_correct_answer = Question.objects.create(
            quiz=cls.quiz,
            word=cls.dictionary,
            options=["random", "2", cls.dictionary.translation],
            user_answer=cls.dictionary.translation
        )
        cls.question_with_incorrect_answer = Question.objects.create(
            quiz=cls.quiz,
            word=cls.dictionary,
            options=["random", "2", cls.dictionary.translation],
            user_answer="random"
        )

    def test_quiz_models_have_correct_object_names(self):
        """Check models' method __str__."""
        str_tests = (
            (str(self.quiz),
             f"Quiz #{self.quiz.id} - {self.student.username}"),
            (str(self.question_with_correct_answer),
             f"Question<{self.question_with_correct_answer.word.word}: "
             f"{self.question_with_correct_answer.word.translation}>"),
        )
        for object, value in str_tests:
            with self.subTest(object=object):
                self.assertEqual(object, value)

    def test_quiz_and_question_properties_and_methods(self):
        """
        Check that properties and methods of models
        Quiz and Question return correct values.
        """
        self.assertEqual(
            self.question_with_correct_answer.is_answer_correct, True
        )
        self.assertEqual(
            self.question_with_incorrect_answer.is_answer_correct, False
        )
        self.assertEqual(self.quiz.count_score(), 1)
