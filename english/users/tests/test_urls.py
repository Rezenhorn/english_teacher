from http import HTTPStatus
from urllib.parse import urljoin

from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

User = get_user_model()


class UsersURLTests(TestCase):
    """URL tests of application Users."""
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.user = User.objects.create_user(username="test_user",
                                            birth_date="2000-01-01")

    def setUp(self):
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_users_url_exists_at_desired_location(self):
        """Test of pages accessibility for guest and authorized user."""
        reverse_names = (
            ("users:signup", False),
            ("users:logout", False),
            ("users:login", False),
            ("users:password_change_form", True),
            ("users:password_change_done", True),
            ("users:password_reset_form", True),
            ("users:password_reset_done", True),
            ("users:password_reset_complete", True)
        )
        for name, auth_status in reverse_names:
            with self.subTest(name=name):
                if auth_status:
                    response = self.authorized_client.get(reverse(name))
                else:
                    response = self.guest_client.get(reverse(name))
                self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_users_pages_uses_correct_template(self):
        """URL-address uses correct template."""
        templates_pages_names = [
            ("users:signup", "users/signup.html"),
            ("users:login", "users/login.html"),
            ("users:password_change_form", "users/password_change_form.html"),
            ("users:password_change_done", "users/password_change_done.html"),
            ("users:password_reset_form", "users/password_reset_form.html"),
            ("users:password_reset_done", "users/password_reset_done.html"),
            ("users:password_reset_complete", (
                "users/password_reset_complete.html"
            )),
            ("users:logout", "users/logged_out.html"),
        ]
        for name, template in templates_pages_names:
            with self.subTest(name=name):
                response = self.authorized_client.get(reverse(name))
                self.assertTemplateUsed(response, template)

    def test_edit_profile_url_redirect_anonymous_on_login(self):
        """Page /edit_profile/ redirect anonymous user to login page."""
        url = reverse("users:edit_profile", kwargs={"user_id": self.user.id})
        redirect = urljoin(
            reverse("users:login"),
            f"?next=/auth/{self.user.id}/edit_profile/"
        )
        response = self.guest_client.get(url, follow=True)
        self.assertRedirects(response, redirect)
