from dictionary.models import Word
from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse
from utils.messages import SMALL_DICTIONARY_FOR_QUIZ_MESSAGE

from ..forms import QUIZ_MODE_CHOICES, WORDS_IN_QUIZ_CHOICES
from ..models import Question, Quiz

User = get_user_model()


class QuizViewsTests(TestCase):
    """Views tests for application Students."""
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.student = User.objects.create_user(
            username="student",
            birth_date="2000-01-01"
        )
        cls.student_non_author = User.objects.create_user(
            username="student_non_author",
            birth_date="2000-01-01"
        )
        cls.word = Word.objects.create(
            word="Test",
            translation="Тест",
            student=cls.student
        )
        cls.quiz = Quiz.objects.create(student=cls.student)
        cls.question = Question.objects.create(
            quiz=cls.quiz,
            word=cls.word,
            options=[cls.word.translation, "random", "1"]
        )

    def setUp(self):
        self.authorized_client = Client()
        self.authorized_client.force_login(self.student)

    def test_redirect_and_message_if_cannot_create_quiz(self):
        """
        Student is redirected to the dictionary and receives
        the message if there are not enough words for a quiz.
        """
        form_data = {
            "quiz_mode": QUIZ_MODE_CHOICES[0][0],
            "number_of_words": WORDS_IN_QUIZ_CHOICES[0][0]
        }
        response = self.authorized_client.post(
            reverse("quiz:quiz_setup",
                    kwargs={"username": self.student.username}),
            data=form_data,
            follow=True
        )
        self.assertRedirects(response, reverse(
            "dictionary:dictionary",
            kwargs={"username": self.student.username}))
        self.assertEqual(Quiz.objects.count(), 0)
        self.assertEqual(Question.objects.count(), 0)

        messages = list(response.context["messages"])
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), SMALL_DICTIONARY_FOR_QUIZ_MESSAGE)

    def test_correct_quiz_result_after_post(self):
        """
        Quiz result page is formed with correct context
        and user anser is saved to model.
        """
        form_data = {
            self.word.word: self.question.options[0]
        }
        response = self.authorized_client.post(
            reverse("quiz:quiz",
                    kwargs={"username": self.student.username,
                            "quiz_id": self.quiz.pk}),
            data=form_data,
            follow=True
        )
        self.assertEqual(
            self.quiz.all_questions[0].user_answer, self.question.options[0]
        )
        self.assertTemplateUsed(response, "quiz/quiz_result.html")
        self.assertEqual(response.context["result_percentage"], 100)
        self.assertEqual(response.context["score"], 1)
