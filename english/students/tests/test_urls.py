from http import HTTPStatus
from urllib.parse import urljoin

from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from ..models import Dictionary, Homework

User = get_user_model()


class StudentsURLTests(TestCase):
    """URL tests for application Students."""
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
        cls.superuser = User.objects.create_superuser(username="superuser")
        cls.dictionary = Dictionary.objects.create(
            word="Test",
            translation="Тест",
            student=cls.student
        )
        cls.homework = Homework.objects.create(
            description="Description of homework",
            student=cls.student
        )

    def setUp(self):
        self.guest_client = Client()
        self.authorized_client = Client()
        self.superuser_client = Client()
        self.authorized_client.force_login(self.student)
        self.superuser_client.force_login(self.superuser)

    def test_reverse_names_equal_urls(self):
        """Test of url and reverse_names match."""
        names = [
            ("/students/", reverse("students:list")),
            (f"/students/{self.student.username}/", reverse(
                "students:student_card",
                kwargs={"username": self.student.username})),
            (f"/students/{self.student.username}/add_homework/", reverse(
                "students:add_homework",
                kwargs={"username": self.student.username})),
            ((f"/students/{self.student.username}/"
              f"edit_homework/{self.homework.pk}/"),
             reverse("students:edit_homework",
                     kwargs={"username": self.student.username,
                             "homework_id": self.homework.pk})),
            ((f"/students/{self.student.username}/"
              f"delete_homework/{self.homework.pk}/"),
             reverse("students:delete_homework",
                     kwargs={"username": self.student.username,
                             "homework_id": self.homework.pk})),
            (f"/students/{self.student.username}/dictionary/",
             reverse("students:dictionary",
                     kwargs={"username": self.student.username})),
            (f"/students/{self.student.username}/dictionary/add_word/",
             reverse("students:add_word",
                     kwargs={"username": self.student.username})),
            (f"/students/{self.student.username}/dictionary/"
             f"edit_word/{self.dictionary.pk}/",
             reverse("students:edit_word",
                     kwargs={"username": self.student.username,
                             "dictionary_id": self.dictionary.pk})),
            (f"/students/{self.student.username}/progress/",
             reverse("students:progress",
                     kwargs={"username": self.student.username})),
        ]
        for url, reverse_name in names:
            with self.subTest(url=url):
                self.assertEqual(url, reverse_name)

    def test_url_exists_at_desired_location(self):
        """Test of pages accessibility for guest and authorized user."""
        reverse_names = [
            (reverse("students:list"), HTTPStatus.OK, True),
            (reverse("students:student_card",
                     kwargs={"username": self.student.username}),
                HTTPStatus.OK,
                False),
            (reverse("students:add_homework",
                     kwargs={"username": self.student.username}),
                HTTPStatus.OK,
                True),
            (reverse("students:edit_homework",
                     kwargs={"username": self.student.username,
                             "homework_id": self.homework.pk}),
                HTTPStatus.OK,
                True),
            (reverse("students:delete_homework",
                     kwargs={"username": self.student.username,
                             "homework_id": self.homework.pk}),
                HTTPStatus.OK,
                True),
            (reverse("students:dictionary",
                     kwargs={"username": self.student.username}),
                HTTPStatus.OK,
                False),
            (reverse("students:add_word",
                     kwargs={"username": self.student.username}),
                HTTPStatus.OK,
                False),
            (reverse("students:edit_word",
                     kwargs={"username": self.student.username,
                             "dictionary_id": self.dictionary.pk}),
                HTTPStatus.OK,
                False),
            (reverse("students:progress",
                     kwargs={"username": self.student.username}),
                HTTPStatus.OK,
                False),
            (("/unexisting_page/"), HTTPStatus.NOT_FOUND, False)
        ]
        for reverse_name, http_status, auth_status in reverse_names:
            with self.subTest(reverse_name=reverse_name):
                if auth_status:
                    response = self.superuser_client.get(reverse_name)
                else:
                    response = self.authorized_client.get(reverse_name)
                self.assertEqual(response.status_code, http_status)

    def test_student_list_edit_homework_redirect_for_non_superuser(self):
        """Admin pages redirect students to index page."""
        reverse_names = (
            reverse("students:list"),
            reverse("students:add_homework",
                    kwargs={"username": self.student.username}),
            reverse("students:edit_homework",
                    kwargs={"username": self.student.username,
                            "homework_id": self.homework.pk})
        )
        for url in reverse_names:
            with self.subTest(url=url):
                response = self.authorized_client.get(url, follow=True)
                self.assertRedirects(response, reverse("about:index"))

    def test_add_word_redirect_for_non_author(self):
        """Test of unavailability of adding a word to
        another student's dictionary.
        """
        self.authorized_client.force_login(self.student_non_author)
        response = self.authorized_client.get(
            reverse("students:add_word",
                    kwargs={"username": self.student.username}),
            follow=True
        )
        self.assertRedirects(response, reverse("about:index"))

    def test_student_url_redirect_anonymous_on_login(self):
        """Pages /student/, /dictionary/, /progress/
        redirect anonymous user to login page.
        """
        url_names = (
            (reverse("students:student_card",
                     kwargs={"username": self.student.username}),
                urljoin(
                    reverse("users:login"),
                    f"?next=/students/{self.student.username}/")),
            (reverse("students:dictionary",
                     kwargs={"username": self.student.username}),
                urljoin(
                    reverse("users:login"),
                    f"?next=/students/{self.student.username}/dictionary/")),
            (reverse("students:progress",
                     kwargs={"username": self.student.username}),
                urljoin(
                    reverse("users:login"),
                    f"?next=/students/{self.student.username}/progress/")),
        )
        for url, redirect in url_names:
            with self.subTest(url=url):
                response = self.guest_client.get(url, follow=True)
                self.assertRedirects(response, redirect)

    def test_pages_uses_correct_template(self):
        """URL-address uses correct template."""
        templates_pages_names = {
            reverse("students:list"): "students/list.html",
            reverse("students:student_card",
                    kwargs={"username": self.student.username}
                    ): "students/student_card.html",
            reverse("students:add_homework",
                    kwargs={"username": self.student.username}
                    ): "students/homework_form.html",
            reverse("students:edit_homework",
                    kwargs={"username": self.student.username,
                            "homework_id": self.homework.pk}
                    ): "students/homework_form.html",
            reverse("students:dictionary",
                    kwargs={"username": self.student.username}
                    ): "students/dictionary.html",
            reverse("students:add_word",
                    kwargs={"username": self.student.username}
                    ): "students/dictionary_form.html",
            reverse("students:edit_word",
                    kwargs={"username": self.student.username,
                            "dictionary_id": self.dictionary.pk}
                    ): "students/dictionary_form.html",
            reverse("students:progress",
                    kwargs={"username": self.student.username}
                    ): "students/progress.html",
            "/unexisting_page/": "core/404.html"
        }
        for reverse_name, template in templates_pages_names.items():
            with self.subTest(reverse_name=reverse_name):
                response = self.superuser_client.get(reverse_name)
                self.assertTemplateUsed(response, template)
