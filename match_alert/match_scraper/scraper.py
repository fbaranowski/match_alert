from home import models as home_models
from match_scraper.logic.main import Scraper
from match_scraper.logic.attributes import WebsiteAttributes, UrlsParams


class ObjectSaver:
    @staticmethod
    def save_teams(league_teams, league_model):
        for team in league_teams:
            obj, created = home_models.Team.objects.get_or_create(
                name=team.name, league=league_model
            )

    @staticmethod
    def save_table(league_table, league_model):
        for element in league_table:
            home_models.LeagueTable.objects.create(
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
                league=league_model,
            )

    @staticmethod
    def save_results(league_results, league_model):
        for result in league_results:
            obj, created = home_models.Result.objects.get_or_create(
                team_1_name=result.team_1_name,
                team_1_score=result.team_1_score,
                team_2_name=result.team_2_name,
                team_2_score=result.team_2_score,
                date=result.date,
                league=league_model,
            )

    @staticmethod
    def save_fixtures(league_fixtures, league_model):
        for fixture in league_fixtures:
            db_fixture = home_models.Fixture.objects.filter(
                team_1_name=fixture.team_1_name, team_2_name=fixture.team_2_name
            ).first()

            if not db_fixture:
                home_models.Fixture.objects.create(
                    team_1_name=fixture.team_1_name,
                    team_2_name=fixture.team_2_name,
                    date=fixture.date,
                    time=fixture.time,
                    league=league_model,
                )
            elif (
                db_fixture
                and db_fixture.date != fixture.date
                or db_fixture.time != fixture.time
            ):
                db_fixture.date = fixture.date
                db_fixture.time = fixture.time
                db_fixture.save()
            else:
                continue


class DatabaseHandler:
    def __init__(self):
        self.premier_league = home_models.League.objects.get(name="Premier League")
        self.la_liga = home_models.League.objects.get(name="La Liga")
        self.bundesliga = home_models.League.objects.get(name="Bundesliga")
        self.serie_a = home_models.League.objects.get(name="Serie A")
        self.ligue_1 = home_models.League.objects.get(name="Ligue 1")

    def fill_team_model(self):
        ObjectSaver.save_teams(
            league_teams=Scraper.get_teams(
                WebsiteAttributes.LEAGUE_CONTAINER_ID["premier_league"]
            ),
            league_model=self.premier_league,
        )
        ObjectSaver.save_teams(
            league_teams=Scraper.get_teams(
                WebsiteAttributes.LEAGUE_CONTAINER_ID["la_liga"]
            ),
            league_model=self.la_liga,
        )
        ObjectSaver.save_teams(
            league_teams=Scraper.get_teams(
                WebsiteAttributes.LEAGUE_CONTAINER_ID["bundesliga"]
            ),
            league_model=self.bundesliga,
        )
        ObjectSaver.save_teams(
            league_teams=Scraper.get_teams(
                WebsiteAttributes.LEAGUE_CONTAINER_ID["serie_a"]
            ),
            league_model=self.serie_a,
        )
        ObjectSaver.save_teams(
            league_teams=Scraper.get_teams(
                WebsiteAttributes.LEAGUE_CONTAINER_ID["ligue_1"]
            ),
            league_model=self.ligue_1,
        )

    def fill_table_model(self):
        home_models.LeagueTable.objects.all().delete()

        ObjectSaver.save_table(
            league_table=Scraper.get_table(
                UrlsParams.league_name_url["premier_league"]
            ),
            league_model=self.premier_league,
        )
        ObjectSaver.save_table(
            league_table=Scraper.get_table(UrlsParams.league_name_url["la_liga"]),
            league_model=self.la_liga,
        )
        ObjectSaver.save_table(
            league_table=Scraper.get_table(UrlsParams.league_name_url["bundesliga"]),
            league_model=self.bundesliga,
        )
        ObjectSaver.save_table(
            league_table=Scraper.get_table(UrlsParams.league_name_url["serie_a"]),
            league_model=self.serie_a,
        )
        ObjectSaver.save_table(
            league_table=Scraper.get_table(UrlsParams.league_name_url["ligue_1"]),
            league_model=self.ligue_1,
        )

    def fill_result_model(self):
        ObjectSaver.save_results(
            league_results=Scraper.get_results(
                UrlsParams.league_name_url["premier_league"]
            ),
            league_model=self.premier_league,
        )
        ObjectSaver.save_results(
            league_results=Scraper.get_results(UrlsParams.league_name_url["la_liga"]),
            league_model=self.la_liga,
        )
        ObjectSaver.save_results(
            league_results=Scraper.get_results(
                UrlsParams.league_name_url["bundesliga"]
            ),
            league_model=self.bundesliga,
        )
        ObjectSaver.save_results(
            league_results=Scraper.get_results(UrlsParams.league_name_url["serie_a"]),
            league_model=self.serie_a,
        )
        ObjectSaver.save_results(
            league_results=Scraper.get_results(UrlsParams.league_name_url["ligue_1"]),
            league_model=self.ligue_1,
        )

    def fill_fixture_model(self):
        ObjectSaver.save_fixtures(
            league_fixtures=Scraper.get_fixtures(
                UrlsParams.league_name_url["premier_league"]
            ),
            league_model=self.premier_league,
        )
        ObjectSaver.save_fixtures(
            league_fixtures=Scraper.get_fixtures(UrlsParams.league_name_url["la_liga"]),
            league_model=self.la_liga,
        )
        ObjectSaver.save_fixtures(
            league_fixtures=Scraper.get_fixtures(
                UrlsParams.league_name_url["bundesliga"]
            ),
            league_model=self.bundesliga,
        )
        ObjectSaver.save_fixtures(
            league_fixtures=Scraper.get_fixtures(UrlsParams.league_name_url["serie_a"]),
            league_model=self.serie_a,
        )
        ObjectSaver.save_fixtures(
            league_fixtures=Scraper.get_fixtures(UrlsParams.league_name_url["ligue_1"]),
            league_model=self.ligue_1,
        )
