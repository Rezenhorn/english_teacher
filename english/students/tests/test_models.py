from django.contrib.auth import get_user_model
from django.test import TestCase

from ..models import Dictionary, Homework, Progress

User = get_user_model()


class StudentsModelTest(TestCase):
    """Model tests of application Students."""
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
        cls.homework = Homework.objects.create(
            description="Description of homework",
            student=cls.student
        )
        cls.progress = Progress.objects.create(
            topic="Test topic",
            student=cls.student
        )

    def test_models_have_correct_object_names(self):
        """Check models' method __str__."""
        str_tests = (
            (str(self.homework), (f"For {self.homework.student}: "
                                  f"{self.homework.description[:40]}")),
            (str(self.dictionary), self.dictionary.word),
            (str(self.progress), (f"{self.progress.topic}: "
                                  f"{self.progress.student}")),
        )
        for object, value in str_tests:
            with self.subTest(object=object):
                self.assertEqual(object, value)
