from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from ..forms import HomeworkForm
from ..models import Homework, Progress

User = get_user_model()


class StudentsViewsTests(TestCase):
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
        cls.superuser = User.objects.create_superuser(username="superuser")
        cls.homework = Homework.objects.create(
            description="Description of homework",
            student=cls.student
        )
        cls.progress = Progress.objects.create(
            topic="Test topic",
            student=cls.student,
            done=True
        )

    def setUp(self):
        self.authorized_client = Client()
        self.superuser_client = Client()
        self.authorized_client.force_login(self.student)
        self.superuser_client.force_login(self.superuser)

    def test_create_pages_show_correct_context(self):
        """Creation pages are formed with correct context."""
        pages = (
            (reverse("students:add_homework",
                     kwargs={"username": self.student.username}),
                HomeworkForm),
        )
        for reverse_name, form in pages:
            with self.subTest(reverse_name=reverse_name):
                response = self.superuser_client.get(reverse_name)
                self.assertIsInstance(response.context.get("form"), form)

    def test_edit_pages_show_correct_context(self):
        """Edit pages are formed with correct context."""
        pages = (
            (reverse("students:edit_homework",
                     kwargs={"username": self.student.username,
                             "homework_id": self.homework.pk}),
                HomeworkForm, self.homework),
        )
        for reverse_name, form, context in pages:
            with self.subTest(reverse_name=reverse_name):
                response = self.superuser_client.get(reverse_name)
                self.assertIsInstance(response.context.get("form"), form)
                self.assertEqual(response.context["form"].instance, context)

    def test_pages_show_correct_context(self):
        """Pages student_card, dictionary, progress are formed
        with correct context.
        """
        pages = (
            (reverse("students:student_card",
                     kwargs={"username": self.student.username}),
                self.homework),
            (reverse("students:progress",
                     kwargs={"username": self.student.username}),
                self.progress)
        )
        for reverse_name, object in pages:
            with self.subTest(reverse_name=reverse_name):
                response = self.authorized_client.get(reverse_name)
                self.assertIn(object, response.context.get("page_obj"))

    def test_objects_not_in_other_student_pages(self):
        """The objects don't end up on another student's pages."""
        pages = (
            (reverse("students:student_card",
                     kwargs={"username": self.student_non_author.username}),
                self.homework),
            (reverse("students:progress",
                     kwargs={"username": self.student_non_author.username}),
                self.progress)
        )
        for reverse_name, object in pages:
            with self.subTest(reverse_name=reverse_name):
                response = self.superuser_client.get(reverse_name)
                self.assertNotIn(object, response.context.get("page_obj"))

    def test_superuser_can_delete_homework(self):
        """Superuser can delete homework and goes to correct page after.."""
        response = self.superuser_client.post(
            reverse("students:delete_homework",
                    kwargs={"username": self.student.username,
                            "homework_id": self.homework.id})
        )
        self.assertRedirects(
            response,
            reverse(
                "students:student_card",
                kwargs={"username": self.student.username}
            )
        )
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Homework.objects.filter(id=self.homework.id).exists())
