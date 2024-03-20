from datetime import datetime
from django.test import TestCase
import home.models as models


class TestModels(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.league = models.League.objects.create(
            name="Test League", slug="test_league"
        )

    def setUp(self):
        self.fixture = models.Fixture.objects.create(
            team_1_name="team1",
            team_2_name="team2",
            date=datetime(year=2024, month=1, day=1).date(),
            time=datetime(year=2024, month=1, day=1, hour=15, minute=0).time(),
            league=self.league,
        )
        self.result = models.Result.objects.create(
            team_1_name="t1",
            team_1_score=1,
            team_2_name="t2",
            team_2_score=2,
            date=datetime(year=2024, month=2, day=15).date(),
            league=self.league,
        )

    def test_fixture_model_content(self):
        self.assertEqual(self.fixture.team_1_name, "team1")
        self.assertEqual(self.fixture.team_2_name, "team2")
        self.assertEqual(self.fixture.date, datetime(year=2024, month=1, day=1).date())
        self.assertEqual(
            self.fixture.time,
            datetime(year=2024, month=1, day=1, hour=15, minute=0).time(),
        )
        self.assertEqual(self.fixture.league, self.league)

    def test_result_model_content(self):
        self.assertEqual(self.result.team_1_name, "t1")
        self.assertEqual(self.result.team_1_score, 1)
        self.assertEqual(self.result.team_2_name, "t2")
        self.assertEqual(self.result.team_2_score, 2)
        self.assertEqual(self.result.date, datetime(year=2024, month=2, day=15).date())
        self.assertEqual(self.result.league, self.league)
