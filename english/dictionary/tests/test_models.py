from django.contrib.auth import get_user_model
from django.test import TestCase

from ..models import Word

User = get_user_model()


class DictionaryModelTest(TestCase):
    """Model tests of application dictionary."""
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.student = User.objects.create_user(username="student",
                                               birth_date="2000-01-01")
        cls.word = Word.objects.create(
            word="Test",
            translation="Тест",
            student=cls.student
        )

    def test_models_have_correct_object_names(self):
        """Check models' method __str__."""
        str_tests = (
            (str(self.word), self.word.word),
        )
        for object, value in str_tests:
            with self.subTest(object=object):
                self.assertEqual(object, value)

    def test_dictionary_word_has_transcription(self):
        """Check auto generation of word transcription."""
        self.assertEqual(self.word.transcription, "tɛst")
