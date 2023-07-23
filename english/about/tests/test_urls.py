from http import HTTPStatus

from django.test import Client, TestCase
from django.urls import reverse


class AboutURLTests(TestCase):
    def setUp(self):
        self.guest_client = Client()

    def test_about_reverse_names_equal_urls(self):
        """Test of URL and reverse_names match."""
        names = [
            ("/", reverse("about:index")),
        ]
        for url, reverse_name in names:
            with self.subTest(url=url):
                self.assertEqual(url, reverse_name)

    def test_about_url_exists_at_desired_location(self):
        """Pages of application About are available for anyone."""
        urls_about = (reverse("about:index"))
        for url in urls_about:
            with self.subTest(url=url):
                response = self.guest_client.get(url)
                self.assertEqual(response.status_code, HTTPStatus.OK)
