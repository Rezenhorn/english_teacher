from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from ..models import Dictionary

User = get_user_model()


class DictionaryFormTests(TestCase):
    """Forms tests of application Dictionary."""
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.student = User.objects.create_user(
            username="student",
            birth_date="2000-01-01"
        )
        cls.dictionary = Dictionary.objects.create(
            word="Test",
            translation="Тест",
            example="Test example",
            student=cls.student
        )

    def setUp(self):
        self.authorized_client = Client()
        self.authorized_client.force_login(self.student)

    def test_create_word(self):
        """Valid form creates object Dictionary."""
        word_count = Dictionary.objects.count()
        form_data = {
            "word": "New",
            "translation": "Новый",
            "example": "New word for test"
        }
        response = self.authorized_client.post(
            reverse("dictionary:add_word",
                    kwargs={"username": self.student.username}),
            data=form_data,
            follow=True
        )
        self.assertRedirects(response, reverse(
            "dictionary:dictionary",
            kwargs={"username": self.student.username}))
        self.assertEqual(Dictionary.objects.count(), word_count + 1)
        self.assertTrue(
            Dictionary.objects.filter(
                word=form_data["word"],
                translation=form_data["translation"],
                example=form_data["example"],
                student=self.student,
            ).exists()
        )

    def test_edit_word(self):
        """Valid form edits object Dictionary."""
        word_count = Dictionary.objects.count()
        form_data = {
            "word": "Edit",
            "translation": "Редактировать",
            "example": "Edited word for test"
        }
        response = self.authorized_client.post(
            reverse("dictionary:edit_word",
                    kwargs={"username": self.student.username,
                            "dictionary_id": self.dictionary.pk}),
            data=form_data,
            follow=True
        )
        self.assertRedirects(response, reverse(
            "dictionary:dictionary",
            kwargs={"username": self.student.username}))
        self.assertEqual(Dictionary.objects.count(), word_count)
        self.assertTrue(
            Dictionary.objects.filter(
                word=form_data["word"],
                translation=form_data["translation"],
                example=form_data["example"],
                student=self.student,
            ).exists()
        )
