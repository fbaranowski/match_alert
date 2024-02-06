from django.contrib import admin
from django.urls import path, include
from home import views as home_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", home_views.HomeView.as_view(), name="home"),
    path(
        "table/<slug:slug>/", home_views.LeagueTableView.as_view(), name="league_table"
    ),
    path(
        "<slug:slug>/teams/", home_views.LeagueTeamsView.as_view(), name="league_teams"
    ),
    path(
        "fixtures/<slug:slug>/",
        home_views.LeagueFixturesView.as_view(),
        name="league_fixtures",
    ),
    path(
        "results/<slug:slug>/",
        home_views.LeagueResultsView.as_view(),
        name="league_results",
    ),
    path(
        "team/fixtures/<slug:team_slug>/",
        home_views.TeamFixturesView.as_view(),
        name="team_fixtures",
    ),
    path(
        "team/results/<slug:team_slug>/",
        home_views.TeamResultsView.as_view(),
        name="team_results",
    ),
    path("auth/", include("users.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
