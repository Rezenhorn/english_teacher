from django.test import Client, TestCase
from django.urls import reverse

from ..forms import CreationForm


class UsersViewsTests(TestCase):
    """Views tests of application Users."""
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

    def setUp(self):
        self.guest_client = Client()

    def test_signup_page_show_correct_context(self):
        """Signup template formed with correct context."""
        response = self.guest_client.get(reverse("users:signup"))
        self.assertIsInstance(response.context.get("form"), CreationForm)
