from datetime import date
from django.views.generic import DetailView
from home.models import League, Fixture, Result, Team


class TeamFixturesView(DetailView):
    model = Team
    template_name = "home/team_fixtures.html"
    context_object_name = "team"
    slug_field = "team_slug"
    slug_url_kwarg = "team_slug"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["leagues"] = League.objects.all()
        fixtures = Fixture.objects.filter(date__gte=date.today())
        filtered_fixtures = (
            fixtures.filter(league=self.object.league, team_1_name=self.object.name)
            | fixtures.filter(league=self.object.league, team_2_name=self.object.name)
            | fixtures.filter(
                league=self.object.league, team_1_name=self.object.short_name
            )
            | fixtures.filter(
                league=self.object.league, team_2_name=self.object.short_name
            )
        )
        context["ordered_fixtures"] = filtered_fixtures.order_by("date")
        return context


class TeamResultsView(DetailView):
    model = Team
    template_name = "home/team_results.html"
    context_object_name = "team"
    slug_field = "team_slug"
    slug_url_kwarg = "team_slug"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["leagues"] = League.objects.all()
        all_results = Result.objects.all()
        filtered_results = (
            all_results.filter(league=self.object.league, team_1_name=self.object.name)
            | all_results.filter(
                league=self.object.league, team_2_name=self.object.name
            )
            | all_results.filter(
                league=self.object.league, team_1_name=self.object.short_name
            )
            | all_results.filter(
                league=self.object.league, team_2_name=self.object.short_name
            )
        )
        context["ordered_results"] = filtered_results.order_by("-date")
        return context
