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
        context["fixtures"] = Fixture.objects.filter(
            league=self.object.id, date__gte=date.today()
        )
        return context

    # TODO
    # def solution():
    #     my_text = "Hello World. Goodbye World!"
    #     occs = {}
    #     for ltr in my_text:
    #         if ltr not in occs.keys():
    #             occs[ltr] = 1
    #         else:
    #             occs[ltr] += 1
    #
    #     my_objs = [obj1, obj2, obj3]
    #     fixtures_by_dates = {}
    #     for obj in my_objs:
    #         if obj.date not in fixtures_by_dates.keys():
    #             fixtures_by_dates[obj.date] = []
    #         else:
    #             fixtures_by_dates[obj.date].append(obj)


class LeagueResultsView(DetailView):
    # DatabaseHandler.fill_result_model()
    model = League
    template_name = "home/league_results.html"
    context_object_name = "league"
    extra_context = {"leagues": League.objects.all()}


class TeamFixturesView(DetailView):
    model = Team
    template_name = "home/team_fixtures.html"
    context_object_name = "team"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # TODO
        # all_fixtures = Fixture.objects.all()
        # filtered_fixtures =
        # filtered_fixtures.order_by(...)

        context["fixtures"] = (
            Fixture.objects.all()
            .filter(league=self.object.league, team_1_name=self.object.name)
            .order_by("date")
            | Fixture.objects.all()
            .filter(league=self.object.league, team_2_name=self.object.name)
            .order_by("date")
            | Fixture.objects.all()
            .filter(league=self.object.league, team_1_name=self.object.short_name)
            .order_by("date")
            | Fixture.objects.all()
            .filter(league=self.object.league, team_2_name=self.object.short_name)
            .order_by("date")
        )

        return context


class TeamResultsView(DetailView):
    model = Team
    template_name = "home/team_results.html"
    context_object_name = "team"

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
