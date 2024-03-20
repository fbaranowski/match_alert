from django.urls import path
from home.views import leagues, teams


urlpatterns = [
    path("", leagues.HomeView.as_view(), name="home"),
    path(
        "<slug:slug>/table/",
        leagues.LeagueTableView.as_view(),
        name="league_table",
    ),
    path(
        "<slug:slug>/teams/",
        leagues.LeagueTeamsView.as_view(),
        name="league_teams",
    ),
    path(
        "<slug:slug>/fixtures/",
        leagues.LeagueFixturesView.as_view(),
        name="league_fixtures",
    ),
    path(
        "<slug:slug>/results/",
        leagues.LeagueResultsView.as_view(),
        name="league_results",
    ),
    path(
        "<slug:team_slug>/team/fixtures/",
        teams.TeamFixturesView.as_view(),
        name="team_fixtures",
    ),
    path(
        "<slug:team_slug>/team/results/",
        teams.TeamResultsView.as_view(),
        name="team_results",
    ),
]
