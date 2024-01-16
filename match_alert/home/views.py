from django.views.generic import ListView, DetailView
from home.models import League, Fixture
from datetime import date


class HomeView(ListView):
    model = League
    template_name = "home/home.html"
    context_object_name = "leagues"


class LeagueTableView(DetailView):
    # DatabaseHandler.fill_table_model()
    model = League
    template_name = "home/league_table.html"
    context_object_name = "league"
    extra_context = {"leagues": League.objects.all()}


class LeagueTeamsView(DetailView):
    # DatabaseHandler.fill_team_model()
    model = League
    template_name = "home/league_teams.html"
    context_object_name = "league"
    extra_context = {"leagues": League.objects.all()}


class LeagueFixturesView(DetailView):
    # DatabaseHandler.fill_fixture_model()
    model = League
    template_name = "home/league_fixtures.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["leagues"] = League.objects.all()
        context["fixtures"] = Fixture.objects.filter(
            league=self.object.id, date__gte=date.today()
        )
        return context


class LeagueResultsView(DetailView):
    # DatabaseHandler.fill_result_model()
    model = League
    template_name = "home/league_results.html"
    context_object_name = "league"
    extra_context = {"leagues": League.objects.all()}
