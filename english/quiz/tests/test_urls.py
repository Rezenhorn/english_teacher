from http import HTTPStatus
from urllib.parse import urljoin

from dictionary.models import Word
from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from ..models import Quiz

User = get_user_model()


class QuizURLTests(TestCase):
    """URL tests for application Quiz."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.student = User.objects.create_user(
            username="student", birth_date="2000-01-01"
        )
        cls.student_non_author = User.objects.create_user(
            username="student_non_author", birth_date="2000-01-01"
        )
        for num in range(3):
            Word.objects.create(
                word=f"Test{num}",
                translation=f"Тест{num}",
                student=cls.student
            )
        cls.quiz = Quiz.objects.create(student=cls.student)

    def setUp(self):
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(self.student)

    def test_quiz_reverse_names_equal_urls(self):
        """Test of URL and reverse_names match."""
        names = [
            (f"/quiz/{self.student.username}/create/",
             reverse("quiz:quiz_setup",
                     kwargs={"username": self.student.username})),
            (f"/quiz/{self.student.username}/{self.quiz.pk}/",
             reverse("quiz:quiz",
                     kwargs={"username": self.student.username,
                             "quiz_id": self.quiz.pk})),
        ]
        for url, reverse_name in names:
            with self.subTest(url=url):
                self.assertEqual(url, reverse_name)

    def test_quiz_url_exists_at_desired_location(self):
        """Test of pages accessibility for authorized user."""
        reverse_names = [
            (reverse("quiz:quiz_setup",
                     kwargs={"username": self.student.username}),
                HTTPStatus.OK),
            (reverse("quiz:quiz",
                     kwargs={"username": self.student.username,
                             "quiz_id": self.quiz.pk}),
                HTTPStatus.OK),
        ]
        for reverse_name, http_status in reverse_names:
            with self.subTest(reverse_name=reverse_name):
                response = self.authorized_client.get(reverse_name)
                self.assertEqual(response.status_code, http_status)

    def test_quiz_redirect_for_non_author(self):
        """Quiz pages redirect another student to index page."""
        self.authorized_client.force_login(self.student_non_author)
        reverse_names = (
            reverse("quiz:quiz_setup",
                    kwargs={"username": self.student.username}),
            reverse("quiz:quiz",
                    kwargs={"username": self.student.username,
                            "quiz_id": self.quiz.pk}),
        )
        for url in reverse_names:
            with self.subTest(url=url):
                response = self.authorized_client.get(url, follow=True)
                self.assertRedirects(response, reverse("about:index"))

    def test_quiz_url_redirect_anonymous_on_login(self):
        """Quiz pages redirect anonymous user to login page."""
        url_names = (
            (
                reverse(
                    "quiz:quiz_setup",
                    kwargs={"username": self.student.username}
                ),
                urljoin(
                    reverse("users:login"),
                    f"?next=/quiz/{self.student.username}/create/",
                ),
            ),
            (
                reverse(
                    "quiz:quiz",
                    kwargs={"username": self.student.username,
                            "quiz_id": self.quiz.pk}
                ),
                urljoin(
                    reverse("users:login"),
                    f"?next=/quiz/{self.student.username}/{self.quiz.pk}/",
                ),
            ),
        )
        for url, redirect in url_names:
            with self.subTest(url=url):
                response = self.guest_client.get(url, follow=True)
                self.assertRedirects(response, redirect)

    def test_quiz_pages_use_correct_templates(self):
        """URL-address uses correct template."""
        templates_pages_names = {
            reverse("quiz:quiz_setup",
                    kwargs={"username": self.student.username}
                    ): "quiz/quiz_setup.html",
            reverse("quiz:quiz",
                    kwargs={"username": self.student.username,
                            "quiz_id": self.quiz.pk}
                    ): "quiz/quiz.html",
        }
        for reverse_name, template in templates_pages_names.items():
            with self.subTest(reverse_name=reverse_name):
                response = self.authorized_client.get(reverse_name)
                self.assertTemplateUsed(response, template)
