from django.test import TestCase
from home.models import League


class TestModels(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.league = League.objects.create(name="Test League", href_str="test_url_name")

    def test_model_content(self):
        self.assertEqual(self.league.name, "Test League")
        self.assertEqual(self.league.href_str, "test_url_name")
