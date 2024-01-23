from django.db import models
from django.utils.text import slugify


class League(models.Model):
    name = models.CharField(max_length=100)
    href_str = models.TextField()
    season = models.CharField(max_length=7, default="2023/24")
    slug = models.SlugField(default="", null=False)

    def __str__(self):
        return self.name


class Team(models.Model):
    name = models.CharField(max_length=75)
    short_name = models.CharField(max_length=30, null=True, blank=True)
    team_slug = models.SlugField(default="", null=False)
    league = models.ForeignKey(League, on_delete=models.CASCADE, related_name="teams")

    def save(self, *args, **kwargs):
        if not self.team_slug:
            self.team_slug = slugify(self.name)
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class LeagueTable(models.Model):
    position = models.PositiveSmallIntegerField()
    team = models.CharField(max_length=75)
    played = models.PositiveSmallIntegerField()
    no_wins = models.PositiveSmallIntegerField()
    no_draws = models.PositiveSmallIntegerField()
    no_losses = models.PositiveSmallIntegerField()
    goals_for = models.PositiveSmallIntegerField()
    goals_against = models.PositiveSmallIntegerField()
    goals_difference = models.SmallIntegerField()
    points = models.SmallIntegerField()
    form = models.CharField(max_length=5)
    league = models.ForeignKey(League, on_delete=models.CASCADE, related_name="table")

    def __str__(self):
        return f"{self.league} Table"


class Fixture(models.Model):
    team_1_name = models.CharField(max_length=75)
    team_2_name = models.CharField(max_length=75)
    date = models.DateField()
    time = models.TimeField()
    league = models.ForeignKey(
        League, on_delete=models.CASCADE, related_name="fixtures"
    )

    def __str__(self):
        return f"Fixture: {self.date}: {self.team_1_name} - {self.team_2_name}"


class Result(models.Model):
    team_1_name = models.CharField(max_length=75)
    team_1_score = models.CharField(max_length=2)
    team_2_name = models.CharField(max_length=75)
    team_2_score = models.CharField(max_length=2)
    date = models.DateField()
    league = models.ForeignKey(League, on_delete=models.CASCADE, related_name="results")

    def __str__(self):
        return f"Result: {self.date}: {self.team_1_name} - {self.team_2_name}"
