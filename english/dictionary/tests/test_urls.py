from http import HTTPStatus
from urllib.parse import urljoin

from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from ..models import Word

User = get_user_model()


class DictionaryURLTests(TestCase):
    """URL tests for application Word."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.student = User.objects.create_user(
            username="student", birth_date="2000-01-01"
        )
        cls.student_non_author = User.objects.create_user(
            username="student_non_author", birth_date="2000-01-01"
        )
        cls.word = Word.objects.create(
            word="Test", translation="Тест", student=cls.student
        )

    def setUp(self):
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(self.student)

    def test_dictionary_reverse_names_equal_urls(self):
        """Test of URL and reverse_names match."""
        names = [
            (f"/dictionary/{self.student.username}/",
             reverse("dictionary:dictionary",
                     kwargs={"username": self.student.username})),
            (f"/dictionary/{self.student.username}/add_word/",
             reverse("dictionary:add_word",
                     kwargs={"username": self.student.username})),
            (f"/dictionary/{self.student.username}/"
             f"edit_word/{self.word.pk}/",
             reverse("dictionary:edit_word",
                     kwargs={"username": self.student.username,
                             "word_id": self.word.pk})),
        ]
        for url, reverse_name in names:
            with self.subTest(url=url):
                self.assertEqual(url, reverse_name)

    def test_dictionary_url_exists_at_desired_location(self):
        """Test of pages accessibility for authorized user."""
        reverse_names = [
            (reverse("dictionary:dictionary",
                     kwargs={"username": self.student.username}),
                HTTPStatus.OK),
            (reverse("dictionary:add_word",
                     kwargs={"username": self.student.username}),
                HTTPStatus.OK),
            (reverse("dictionary:edit_word",
                     kwargs={"username": self.student.username,
                             "word_id": self.word.pk}),
                HTTPStatus.OK),
        ]
        for reverse_name, http_status in reverse_names:
            with self.subTest(reverse_name=reverse_name):
                response = self.authorized_client.get(reverse_name)
                self.assertEqual(response.status_code, http_status)

    def test_dictionary_redirect_for_non_author(self):
        """Word pages redirect another student to index page."""
        self.authorized_client.force_login(self.student_non_author)
        reverse_names = (
            reverse("dictionary:add_word",
                    kwargs={"username": self.student.username}),
            reverse("dictionary:download_dictionary",
                    kwargs={"username": self.student.username}),
            reverse("dictionary:edit_word",
                    kwargs={"username": self.student.username,
                            "word_id": self.word.pk}),
        )
        for url in reverse_names:
            with self.subTest(url=url):
                response = self.authorized_client.get(url, follow=True)
                self.assertRedirects(response, reverse("about:index"))

    def test_dictionary_url_redirect_anonymous_on_login(self):
        """Word pages redirect anonymous user to login page."""
        url_names = (
            (
                reverse(
                    "dictionary:dictionary",
                    kwargs={"username": self.student.username}
                ),
                urljoin(
                    reverse("users:login"),
                    f"?next=/dictionary/{self.student.username}/",
                ),
            ),
            (
                reverse(
                    "dictionary:add_word",
                    kwargs={"username": self.student.username}
                ),
                urljoin(
                    reverse("users:login"),
                    f"?next=/dictionary/{self.student.username}/add_word/",
                ),
            ),
            (
                reverse(
                    "dictionary:download_dictionary",
                    kwargs={"username": self.student.username},
                ),
                urljoin(
                    reverse("users:login"),
                    f"?next=/dictionary/{self.student.username}/download",
                ),
            ),
            (
                reverse(
                    "dictionary:edit_word",
                    kwargs={
                        "username": self.student.username,
                        "word_id": self.word.pk,
                    },
                ),
                urljoin(
                    reverse("users:login"),
                    (f"?next=/dictionary/{self.student.username}"
                     f"/edit_word/{self.word.id}/"),
                ),
            ),
        )
        for url, redirect in url_names:
            with self.subTest(url=url):
                response = self.guest_client.get(url, follow=True)
                self.assertRedirects(response, redirect)

    def test_dictionary_pages_use_correct_templates(self):
        """URL-address uses correct template."""
        templates_pages_names = {
            reverse("dictionary:dictionary",
                    kwargs={"username": self.student.username}
                    ): "dictionary/dictionary.html",
            reverse("dictionary:add_word",
                    kwargs={"username": self.student.username}
                    ): "dictionary/dictionary_form.html",
            reverse("dictionary:edit_word",
                    kwargs={"username": self.student.username,
                            "word_id": self.word.pk}
                    ): "dictionary/dictionary_form.html",
        }
        for reverse_name, template in templates_pages_names.items():
            with self.subTest(reverse_name=reverse_name):
                response = self.authorized_client.get(reverse_name)
                self.assertTemplateUsed(response, template)
