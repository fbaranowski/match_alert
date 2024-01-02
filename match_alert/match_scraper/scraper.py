from logic.main import Scraper
from logic.attributes import WebsiteAttributes, UrlsParams
from home import models as home_models


class DatabaseHandler:
    PREMIER_LEAGUE = home_models.League.objects.get(
        name="Premier League", season="2023/24"
    )
    LA_LIGA = home_models.League.objects.get(name="La Liga", season="2023/24")
    BUNDESLIGA = home_models.League.objects.get(name="Bundesliga", season="2023/24")
    SERIE_A = home_models.League.objects.get(name="Serie A", season="2023/24")
    LIGUE_1 = home_models.League.objects.get(name="Ligue 1", season="2023/24")

    @staticmethod
    def fill_team_model():
        premier_league_teams = Scraper.get_teams(
            WebsiteAttributes.LEAGUE_CONTAINER_ID["premier_league"]
        )
        la_liga_teams = Scraper.get_teams(
            WebsiteAttributes.LEAGUE_CONTAINER_ID["la_liga"]
        )
        bundesliga_teams = Scraper.get_teams(
            WebsiteAttributes.LEAGUE_CONTAINER_ID["bundesliga"]
        )
        serie_a_teams = Scraper.get_teams(
            WebsiteAttributes.LEAGUE_CONTAINER_ID["serie_a"]
        )
        ligue_1_teams = Scraper.get_teams(
            WebsiteAttributes.LEAGUE_CONTAINER_ID["ligue_1"]
        )

        for team in premier_league_teams:
            obj, created = home_models.Team.objects.get_or_create(
                name=team.name, league=DatabaseHandler.PREMIER_LEAGUE
            )
        for team in la_liga_teams:
            obj, created = home_models.Team.objects.get_or_create(
                name=team.name, league=DatabaseHandler.LA_LIGA
            )
        for team in bundesliga_teams:
            obj, created = home_models.Team.objects.get_or_create(
                name=team.name, league=DatabaseHandler.BUNDESLIGA
            )
        for team in serie_a_teams:
            obj, created = home_models.Team.objects.get_or_create(
                name=team.name, league=DatabaseHandler.SERIE_A
            )
        for team in ligue_1_teams:
            obj, created = home_models.Team.objects.get_or_create(
                name=team.name, league=DatabaseHandler.LIGUE_1
            )

    @staticmethod
    def fill_table_model():
        premier_league_table = Scraper.get_table(
            UrlsParams.league_name_url["premier_league"]
        )
        la_liga_table = Scraper.get_table(UrlsParams.league_name_url["la_liga"])
        bundesliga_table = Scraper.get_table(UrlsParams.league_name_url["bundesliga"])
        serie_a_table = Scraper.get_table(UrlsParams.league_name_url["serie_a"])
        ligue_1_table = Scraper.get_table(UrlsParams.league_name_url["ligue_1"])

        for element in premier_league_table:
            obj, created = home_models.LeagueTable.objects.update_or_create(
                position=element.position,
                team=element.team,
                played=element.played,
                no_wins=element.won,
                no_draws=element.drew,
                no_losses=element.lost,
                goals_for=element.goals_for,
                goals_against=element.goals_against,
                goals_difference=element.goal_difference,
                points=element.points,
                form=element.form,
                league=DatabaseHandler.PREMIER_LEAGUE,
            )
        for element in la_liga_table:
            obj, created = home_models.LeagueTable.objects.update_or_create(
                position=element.position,
                team=element.team,
                played=element.played,
                no_wins=element.won,
                no_draws=element.drew,
                no_losses=element.lost,
                goals_for=element.goals_for,
                goals_against=element.goals_against,
                goals_difference=element.goal_difference,
                points=element.points,
                form=element.form,
                league=DatabaseHandler.LA_LIGA,
            )
        for element in bundesliga_table:
            obj, created = home_models.LeagueTable.objects.update_or_create(
                position=element.position,
                team=element.team,
                played=element.played,
                no_wins=element.won,
                no_draws=element.drew,
                no_losses=element.lost,
                goals_for=element.goals_for,
                goals_against=element.goals_against,
                goals_difference=element.goal_difference,
                points=element.points,
                form=element.form,
                league=DatabaseHandler.BUNDESLIGA,
            )
        for element in serie_a_table:
            obj, created = home_models.LeagueTable.objects.update_or_create(
                position=element.position,
                team=element.team,
                played=element.played,
                no_wins=element.won,
                no_draws=element.drew,
                no_losses=element.lost,
                goals_for=element.goals_for,
                goals_against=element.goals_against,
                goals_difference=element.goal_difference,
                points=element.points,
                form=element.form,
                league=DatabaseHandler.SERIE_A,
            )
        for element in ligue_1_table:
            obj, created = home_models.LeagueTable.objects.update_or_create(
                position=element.position,
                team=element.team,
                played=element.played,
                no_wins=element.won,
                no_draws=element.drew,
                no_losses=element.lost,
                goals_for=element.goals_for,
                goals_against=element.goals_against,
                goals_difference=element.goal_difference,
                points=element.points,
                form=element.form,
                league=DatabaseHandler.LIGUE_1,
            )

    @staticmethod
    def fill_result_model():
        premier_league_results = Scraper.get_results(
            UrlsParams.league_name_url["premier_league"]
        )
        la_liga_results = Scraper.get_results(UrlsParams.league_name_url["la_liga"])
        bundesliga_results = Scraper.get_results(
            UrlsParams.league_name_url["bundesliga"]
        )
        serie_a_results = Scraper.get_results(UrlsParams.league_name_url["serie_a"])
        ligue_1_results = Scraper.get_results(UrlsParams.league_name_url["ligue_1"])

        for result in premier_league_results:
            obj, created = home_models.Result.objects.get_or_create(
                team_1_name=result.team_1_name,
                team_1_score=result.team_1_score,
                team_2_name=result.team_2_name,
                team_2_score=result.team_2_score,
                date=result.date,
                league=DatabaseHandler.PREMIER_LEAGUE,
            )
        for result in la_liga_results:
            obj, created = home_models.Result.objects.get_or_create(
                team_1_name=result.team_1_name,
                team_1_score=result.team_1_score,
                team_2_name=result.team_2_name,
                team_2_score=result.team_2_score,
                date=result.date,
                league=DatabaseHandler.LA_LIGA,
            )
        for result in bundesliga_results:
            obj, created = home_models.Result.objects.get_or_create(
                team_1_name=result.team_1_name,
                team_1_score=result.team_1_score,
                team_2_name=result.team_2_name,
                team_2_score=result.team_2_score,
                date=result.date,
                league=DatabaseHandler.BUNDESLIGA,
            )
        for result in serie_a_results:
            obj, created = home_models.Result.objects.get_or_create(
                team_1_name=result.team_1_name,
                team_1_score=result.team_1_score,
                team_2_name=result.team_2_name,
                team_2_score=result.team_2_score,
                date=result.date,
                league=DatabaseHandler.SERIE_A,
            )
        for result in ligue_1_results:
            obj, created = home_models.Result.objects.get_or_create(
                team_1_name=result.team_1_name,
                team_1_score=result.team_1_score,
                team_2_name=result.team_2_name,
                team_2_score=result.team_2_score,
                date=result.date,
                league=DatabaseHandler.LIGUE_1,
            )

    @staticmethod
    def fill_fixture_model():
        premier_league_fixtures = Scraper.get_fixtures(
            UrlsParams.league_name_url["premier_league"]
        )
        la_liga_fixtures = Scraper.get_fixtures(UrlsParams.league_name_url["la_liga"])
        bundesliga_fixtures = Scraper.get_fixtures(
            UrlsParams.league_name_url["bundesliga"]
        )
        serie_a_fixtures = Scraper.get_fixtures(UrlsParams.league_name_url["serie_a"])
        ligue_1_fixtures = Scraper.get_fixtures(UrlsParams.league_name_url["ligue_1"])

        for fixture in premier_league_fixtures:
            obj, created = home_models.Fixture.objects.get_or_create(
                team_1_name=fixture.team_1_name,
                team_2_name=fixture.team_2_name,
                date=fixture.date,
                time=fixture.time,
                league=DatabaseHandler.PREMIER_LEAGUE,
            )
        for fixture in la_liga_fixtures:
            obj, created = home_models.Fixture.objects.get_or_create(
                team_1_name=fixture.team_1_name,
                team_2_name=fixture.team_2_name,
                date=fixture.date,
                time=fixture.time,
                league=DatabaseHandler.LA_LIGA,
            )
        for fixture in bundesliga_fixtures:
            obj, created = home_models.Fixture.objects.get_or_create(
                team_1_name=fixture.team_1_name,
                team_2_name=fixture.team_2_name,
                date=fixture.date,
                time=fixture.time,
                league=DatabaseHandler.BUNDESLIGA,
            )
        for fixture in serie_a_fixtures:
            obj, created = home_models.Fixture.objects.get_or_create(
                team_1_name=fixture.team_1_name,
                team_2_name=fixture.team_2_name,
                date=fixture.date,
                time=fixture.time,
                league=DatabaseHandler.SERIE_A,
            )
        for fixture in ligue_1_fixtures:
            obj, created = home_models.Fixture.objects.get_or_create(
                team_1_name=fixture.team_1_name,
                team_2_name=fixture.team_2_name,
                date=fixture.date,
                time=fixture.time,
                league=DatabaseHandler.LIGUE_1,
            )
