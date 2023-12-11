from django.test import TestCase
from django.urls import reverse


class TestHomeView(TestCase):
    def test_url_at_correct_endpoint(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

    def test_url_available_by_name(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)

    def test_template_name_is_correct(self):
        response = self.client.get(reverse("home"))
        self.assertTemplateUsed(response, "home/home.html")

    def test_template_content(self):
        response = self.client.get(reverse("home"))
        self.assertContains(response, "<h1>MatchAlert</h1>")
