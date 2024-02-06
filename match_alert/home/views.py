from django.views.generic import ListView, DetailView
from home.models import League, Fixture, Team, Result
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
        fixtures_list = Fixture.objects.filter(
            league=self.object.id, date__gte=date.today()
        )
        fixtures_by_date = {}
        for fixt in fixtures_list:
            if fixt.date not in fixtures_by_date.keys():
                fixtures_by_date[fixt.date] = [fixt]
            else:
                fixtures_by_date[fixt.date].append(fixt)
        context["fixtures_dict"] = fixtures_by_date
        return context


class LeagueResultsView(DetailView):
    # DatabaseHandler.fill_result_model()
    model = League
    template_name = "home/league_results.html"
    context_object_name = "league"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["leagues"] = League.objects.all()
        results_list = Result.objects.filter(league=self.object.id)
        results_by_date = {}
        for result in results_list:
            if result.date not in results_by_date.keys():
                results_by_date[result.date] = [result]
            else:
                results_by_date[result.date].append(result)
        context["results_dict"] = results_by_date
        return context


class TeamFixturesView(DetailView):
    model = Team
    template_name = "home/team_fixtures.html"
    context_object_name = "team"
    slug_field = "team_slug"
    slug_url_kwarg = "team_slug"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        all_fixtures = Fixture.objects.all()
        filtered_fixtures = (
            all_fixtures.filter(league=self.object.league, team_1_name=self.object.name)
            | all_fixtures.filter(
                league=self.object.league, team_2_name=self.object.name
            )
            | all_fixtures.filter(
                league=self.object.league, team_1_name=self.object.short_name
            )
            | all_fixtures.filter(
                league=self.object.league, team_2_name=self.object.short_name
            )
        )
        context["ordered_fixtures"] = filtered_fixtures.order_by("date")
        # context["fixtures"] = (
        #     Fixture.objects.all()
        #     .filter(league=self.object.league, team_1_name=self.object.name)
        #     .order_by("date")
        #     | Fixture.objects.all()
        #     .filter(league=self.object.league, team_2_name=self.object.name)
        #     .order_by("date")
        #     | Fixture.objects.all()
        #     .filter(league=self.object.league, team_1_name=self.object.short_name)
        #     .order_by("date")
        #     | Fixture.objects.all()
        #     .filter(league=self.object.league, team_2_name=self.object.short_name)
        #     .order_by("date")
        # )

        return context


class TeamResultsView(DetailView):
    model = Team
    template_name = "home/team_results.html"
    context_object_name = "team"
    slug_field = "team_slug"
    slug_url_kwarg = "team_slug"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["results"] = (
            Result.objects.all()
            .filter(league=self.object.league, team_1_name=self.object.name)
            .order_by("-date")
            | Result.objects.all()
            .filter(league=self.object.league, team_2_name=self.object.name)
            .order_by("-date")
            | Result.objects.all()
            .filter(league=self.object.league, team_1_name=self.object.short_name)
            .order_by("-date")
            | Result.objects.all()
            .filter(league=self.object.league, team_2_name=self.object.short_name)
            .order_by("-date")
        )
        return context
