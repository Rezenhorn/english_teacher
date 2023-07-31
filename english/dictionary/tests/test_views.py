from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from ..forms import DictionaryForm
from ..models import Word

User = get_user_model()


class DictionaryViewsTests(TestCase):
    """Views tests for application dictionary."""
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
        cls.word = Word.objects.create(
            word="Test",
            translation="Тест",
            example="Test example",
            student=cls.student
        )

    def setUp(self):
        self.authorized_client = Client()
        self.superuser_client = Client()
        self.authorized_client.force_login(self.student)
        self.superuser_client.force_login(self.superuser)

    def test_create_pages_show_correct_context(self):
        """Word creation page is formed with correct context."""
        pages = (
            (reverse("dictionary:add_word",
                     kwargs={"username": self.student.username}),
                DictionaryForm),
        )
        for reverse_name, form in pages:
            with self.subTest(reverse_name=reverse_name):
                response = self.superuser_client.get(reverse_name)
                self.assertIsInstance(response.context.get("form"), form)

    def test_edit_pages_show_correct_context(self):
        """Word edit page is formed with correct context."""
        pages = (
            (reverse("dictionary:edit_word",
                     kwargs={"username": self.student.username,
                             "word_id": self.word.pk}),
                DictionaryForm, self.word),
        )
        for reverse_name, form, context in pages:
            with self.subTest(reverse_name=reverse_name):
                response = self.superuser_client.get(reverse_name)
                self.assertIsInstance(response.context.get("form"), form)
                self.assertEqual(response.context["form"].instance, context)

    def test_pages_show_correct_context(self):
        """Word page is formed with correct context."""
        pages = (
            (reverse("dictionary:dictionary",
                     kwargs={"username": self.student.username}),
                self.word),
        )
        for reverse_name, object in pages:
            with self.subTest(reverse_name=reverse_name):
                response = self.authorized_client.get(reverse_name)
                self.assertIn(object, response.context.get("page_obj"))

    def test_objects_not_in_other_student_pages(self):
        """The objects don't end up on another student's pages."""
        pages = (
            (reverse("dictionary:dictionary",
                     kwargs={"username": self.student_non_author.username}),
                self.word),
        )
        for reverse_name, object in pages:
            with self.subTest(reverse_name=reverse_name):
                response = self.superuser_client.get(reverse_name)
                self.assertNotIn(object, response.context.get("page_obj"))

    def test_dictionary_download(self):
        """Test for student's dictionary download."""
        response = self.authorized_client.get(
            reverse("dictionary:download_dictionary",
                    kwargs={"username": self.student.username}))
        self.assertEqual(
            response.get("Content-Disposition"),
            f"attachment; filename={self.student.username}'s_dict.xls"
        )

    def test_user_can_delete_word(self):
        """
        User can delete word from Word
        and is redirected to correct page after.
        """
        response = self.authorized_client.post(
            reverse("dictionary:delete_word",
                    kwargs={"username": self.student.username,
                            "word_id": self.word.id})
        )
        self.assertRedirects(
            response,
            reverse(
                "dictionary:dictionary",
                kwargs={"username": self.student.username}
            )
        )
        self.assertEqual(response.status_code, 302)
        self.assertFalse(
            Word.objects.filter(id=self.word.id).exists()
        )
