from dictionary.models import Dictionary
from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from ..forms import QUIZ_MODE_CHOICES, WORDS_IN_QUIZ_CHOICES
from ..models import Quiz

User = get_user_model()


class QuizFormTests(TestCase):
    """Forms tests of application Dictionary."""
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.student = User.objects.create_user(
            username="student",
            birth_date="2000-01-01"
        )
        for num in range(3):
            Dictionary.objects.create(
                word=f"Test{num}",
                translation=f"Тест{num}",
                student=cls.student
            )

    def setUp(self):
        self.authorized_client = Client()
        self.authorized_client.force_login(self.student)

    def test_create_quiz(self):
        """
        Valid form creates object Quiz.
        Covers all quiz modes.
        """
        quiz_count = Quiz.objects.count()
        for mode in QUIZ_MODE_CHOICES:
            with self.subTest(mode=mode[0]):
                form_data = {
                    "quiz_mode": mode[0],
                    "number_of_words": WORDS_IN_QUIZ_CHOICES[0][0]
                }
                response = self.authorized_client.post(
                    reverse("quiz:quiz_setup",
                            kwargs={"username": self.student.username}),
                    data=form_data,
                    follow=True
                )

                self.assertRedirects(response, reverse(
                    "quiz:quiz",
                    kwargs={"username": self.student.username,
                            "quiz_id": self.student.quizzes.latest("pk").pk}))
                self.assertEqual(Quiz.objects.count(), quiz_count + 1)
                self.assertTrue(
                    Quiz.objects.filter(student=self.student).exists()
                )
