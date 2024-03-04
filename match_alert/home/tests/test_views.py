from django.test import TestCase
from django.urls import reverse
import home.models as home_models


class TestHomeView(TestCase):
    def setUp(self):
        self.response = self.client.get(reverse("home"))

    def test_url_at_correct_endpoint(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

    def test_url_available_by_name(self):
        self.assertEqual(self.response.status_code, 200)

    def test_template_name_is_correct(self):
        self.assertTemplateUsed(self.response, "home/home.html")

    def test_template_content(self):
        self.assertContains(self.response, "<h1>MatchAlert</h1>")


class TestLeagueTableView(TestCase):
    def setUp(self):
        test_league = home_models.League.objects.create(name="league", slug="league")
        test_table = home_models.LeagueTable.objects.create(
            position=1,
            team="team",
            played=1,
            no_wins=3,
            no_draws=1,
            no_losses=1,
            goals_for=5,
            goals_against=2,
            goals_difference=3,
            points=4,
            form="WDDLW",
            league=test_league,
        )
        self.response = self.client.get(
            reverse("league_table", kwargs={"slug": test_table.league.slug})
        )

    def test_url_at_correct_endpoint(self):
        response = self.client.get("/league/table/")
        self.assertEqual(response.status_code, 200)

    def test_url_available_by_name(self):
        self.assertEqual(self.response.status_code, 200)

    def test_template_name_is_correct(self):
        self.assertTemplateUsed(self.response, "home/league_table.html")

    def test_template_content(self):
        self.assertContains(self.response, "<td>WDDLW</td>")


class TestLeagueTeamsView(TestCase):
    def setUp(self):
        test_league = home_models.League.objects.create(
            name="test_league", slug="league"
        )
        self.response = self.client.get(
            reverse("league_teams", kwargs={"slug": test_league.slug})
        )

    def test_url_at_correct_endpoint(self):
        response = self.client.get("/league/teams/")
        self.assertEqual(response.status_code, 200)

    def test_url_available_by_name(self):
        self.assertEqual(self.response.status_code, 200)

    def test_template_name_is_correct(self):
        self.assertTemplateUsed(self.response, "home/league_teams.html")

    def test_template_content(self):
        self.assertContains(self.response, "<h1>test_league Teams</h1>")


class TestLeagueFixturesView(TestCase):
    def setUp(self):
        test_league = home_models.League.objects.create(
            name="test_league", slug="league"
        )
        self.response = self.client.get(
            reverse("league_fixtures", kwargs={"slug": test_league.slug})
        )

    def test_url_at_correct_endpoint(self):
        response = self.client.get("/league/fixtures/")
        self.assertEqual(response.status_code, 200)

    def test_url_available_by_name(self):
        self.assertEqual(self.response.status_code, 200)

    def test_template_name_is_correct(self):
        self.assertTemplateUsed(self.response, "home/league_fixtures.html")

    def test_template_content(self):
        self.assertContains(self.response, "<h1>test_league Fixtures</h1>")


class TestLeagueResultsView(TestCase):
    def setUp(self):
        test_league = home_models.League.objects.create(
            name="test_league", slug="league"
        )
        self.response = self.client.get(
            reverse("league_results", kwargs={"slug": test_league.slug})
        )

    def test_url_at_correct_endpoint(self):
        response = self.client.get("/league/results/")
        self.assertEqual(response.status_code, 200)

    def test_url_available_by_name(self):
        self.assertEqual(self.response.status_code, 200)

    def test_template_name_is_correct(self):
        self.assertTemplateUsed(self.response, "home/league_results.html")

    def test_template_content(self):
        self.assertContains(self.response, "<h1>test_league Results</h1>")


class TestTeamFixturesView(TestCase):
    def setUp(self):
        test_league = home_models.League.objects.create(name="league", slug="league")
        test_team = home_models.Team.objects.create(
            name="test_team", short_name="t", team_slug="test_team", league=test_league
        )
        self.response = self.client.get(
            reverse("team_fixtures", kwargs={"team_slug": test_team.team_slug})
        )

    def test_url_at_correct_endpoint(self):
        response = self.client.get("/test_team/team/fixtures/")
        self.assertEqual(response.status_code, 200)

    def test_url_available_by_name(self):
        self.assertEqual(self.response.status_code, 200)

    def test_template_name_is_correct(self):
        self.assertTemplateUsed(self.response, "home/team_fixtures.html")

    def test_template_content(self):
        self.assertContains(self.response, "<h1>test_team Fixtures</h1>")


class TestTeamResultsView(TestCase):
    def setUp(self):
        test_league = home_models.League.objects.create(name="league", slug="league")
        test_team = home_models.Team.objects.create(
            name="test_team", short_name="t", team_slug="test_team", league=test_league
        )
        self.response = self.client.get(
            reverse("team_results", kwargs={"team_slug": test_team.team_slug})
        )

    def test_url_at_correct_endpoint(self):
        response = self.client.get("/test_team/team/results/")
        self.assertEqual(response.status_code, 200)

    def test_url_available_by_name(self):
        self.assertEqual(self.response.status_code, 200)

    def test_template_name_is_correct(self):
        self.assertTemplateUsed(self.response, "home/team_results.html")

    def test_template_content(self):
        self.assertContains(self.response, "<h1>test_team Results</h1>")
