import datetime

from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from ..models import Dictionary, Homework

User = get_user_model()


class StudentsFormTests(TestCase):
    """Forms tests of application Students."""
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.student = User.objects.create_user(
            username="student",
            birth_date="2000-01-01"
        )
        cls.superuser = User.objects.create_superuser(username="superuser")
        cls.dictionary = Dictionary.objects.create(
            word="Test",
            translation="Тест",
            example="Test example",
            student=cls.student
        )
        cls.homework = Homework.objects.create(
            description="Description of homework",
            student=cls.student
        )

    def setUp(self):
        self.authorized_client = Client()
        self.superuser_client = Client()
        self.authorized_client.force_login(self.student)
        self.superuser_client.force_login(self.superuser)

    def test_create_homework(self):
        """Valid form creates object Homework."""
        homework_count = Homework.objects.count()
        form_data = {
            "description": "New test homework",
            "date": datetime.date.today(),
        }
        response = self.superuser_client.post(
            reverse("students:add_homework",
                    kwargs={"username": self.student.username}),
            data=form_data,
            follow=True
        )
        self.assertRedirects(response, reverse(
            "students:student_card",
            kwargs={"username": self.student.username}))
        self.assertEqual(Homework.objects.count(), homework_count + 1)
        self.assertTrue(
            Homework.objects.filter(
                description=form_data["description"],
                date=form_data["date"],
                student=self.student,
                done=False
            ).exists()
        )

    def test_edit_homework(self):
        """Valid form edits object Homework."""
        homework_count = Homework.objects.count()
        form_data = {
            "description": "Edited test homework",
            "date": datetime.date.today() + datetime.timedelta(days=1),
        }
        response = self.superuser_client.post(
            reverse("students:edit_homework",
                    kwargs={"username": self.student.username,
                            "homework_id": self.homework.pk}),
            data=form_data,
            follow=True
        )
        self.assertRedirects(response, reverse(
            "students:student_card",
            kwargs={"username": self.student.username}))
        self.assertEqual(Homework.objects.count(), homework_count)
        self.assertTrue(
            Homework.objects.filter(
                description=form_data["description"],
                date=form_data["date"],
                student=self.student,
                done=False
            ).exists()
        )

    def test_create_word(self):
        """Valid form creates object Dictionary."""
        word_count = Dictionary.objects.count()
        form_data = {
            "word": "New",
            "translation": "Новый",
            "example": "New word for test"
        }
        response = self.authorized_client.post(
            reverse("students:add_word",
                    kwargs={"username": self.student.username}),
            data=form_data,
            follow=True
        )
        self.assertRedirects(response, reverse(
            "students:dictionary",
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
            reverse("students:edit_word",
                    kwargs={"username": self.student.username,
                            "dictionary_id": self.dictionary.pk}),
            data=form_data,
            follow=True
        )
        self.assertRedirects(response, reverse(
            "students:dictionary",
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
