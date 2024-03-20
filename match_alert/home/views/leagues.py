from datetime import date
from django.views.generic import ListView, DetailView
from home.models import League, Fixture, Result


class HomeView(ListView):
    model = League
    template_name = "home/home.html"
    context_object_name = "leagues"


class LeagueTableView(DetailView):
    model = League
    template_name = "home/league_table.html"
    context_object_name = "league"
    extra_context = {"leagues": League.objects.all()}


class LeagueTeamsView(DetailView):
    model = League
    template_name = "home/league_teams.html"
    context_object_name = "league"
    extra_context = {"leagues": League.objects.all()}


class LeagueFixturesView(DetailView):
    model = League
    template_name = "home/league_fixtures.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["leagues"] = League.objects.all()
        fixtures_list = Fixture.objects.filter(
            league=self.object.id, date__gte=date.today()
        ).order_by("date")
        fixtures_by_date = {}
        for fixt in fixtures_list:
            if fixt.date not in fixtures_by_date.keys():
                fixtures_by_date[fixt.date] = [fixt]
            else:
                fixtures_by_date[fixt.date].append(fixt)
        context["fixtures_dict"] = fixtures_by_date
        return context


class LeagueResultsView(DetailView):
    model = League
    template_name = "home/league_results.html"
    context_object_name = "league"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["leagues"] = League.objects.all()
        results_list = Result.objects.filter(league=self.object.id).order_by("-date")
        results_by_date = {}
        for result in results_list:
            if result.date not in results_by_date.keys():
                results_by_date[result.date] = [result]
            else:
                results_by_date[result.date].append(result)
        context["results_dict"] = results_by_date
        return context
