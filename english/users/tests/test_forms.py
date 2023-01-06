from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

User = get_user_model()


class UsersFormTests(TestCase):
    """Forms tests of application Users."""
    def setUp(self):
        self.guest_client = Client()

    def test_create_user(self):
        """Valid form creates User."""
        users_count = User.objects.count()
        form_data = {
            "username": "test_user",
            "first_name": "First",
            "last_name": "Last",
            "password1": "789654123jJ",
            "password2": "789654123jJ",
            "birth_date": "2000-01-01",
            "email": "example@email.org"
        }
        response = self.guest_client.post(
            reverse("users:signup"),
            data=form_data,
            follow=True
        )
        self.assertRedirects(response, reverse("about:index"))
        self.assertEqual(User.objects.count(), users_count + 1)
        self.assertTrue(
            User.objects.filter(username=form_data["username"]).exists()
        )
