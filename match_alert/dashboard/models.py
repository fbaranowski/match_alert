from django.db import models
from home.models import League


class Team(models.Model):
    name = models.CharField(max_length=75)
    short_name = models.CharField(max_length=30, null=True, blank=True)
    league = models.ForeignKey(League, on_delete=models.CASCADE, related_name="teams")

    def __str__(self):
        return self.name


class Table(models.Model):
    position = models.CharField(max_length=2)
    team = models.CharField(max_length=75)
    played = models.CharField(max_length=2)
    won = models.CharField(max_length=2)
    drew = models.CharField(max_length=2)
    lost = models.CharField(max_length=2)
    goals_for = models.CharField(max_length=3)
    goals_against = models.CharField(max_length=3)
    goal_difference = models.CharField(max_length=3)
    points = models.CharField(max_length=3)
    form = models.CharField(max_length=5)
    league = models.ForeignKey(League, on_delete=models.CASCADE, related_name="tables")

    def __str__(self):
        return f"{self.league} Table"


class Fixture(models.Model):
    team_1_name = models.CharField(max_length=75)
    team_2_name = models.CharField(max_length=75)
    date = models.DateField()
    time = models.CharField(max_length=5)
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
