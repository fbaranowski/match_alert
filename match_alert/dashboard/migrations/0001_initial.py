# Generated by Django 4.2.7 on 2023-12-18 21:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("home", "0002_league_season"),
    ]

    operations = [
        migrations.CreateModel(
            name="Teams",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=75)),
                ("short_name", models.CharField(blank=True, max_length=30, null=True)),
                (
                    "league",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="teams",
                        to="home.league",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Tables",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("position", models.CharField(max_length=2)),
                ("team", models.CharField(max_length=75)),
                ("played", models.CharField(max_length=2)),
                ("won", models.CharField(max_length=2)),
                ("drew", models.CharField(max_length=2)),
                ("lost", models.CharField(max_length=2)),
                ("goals_for", models.CharField(max_length=3)),
                ("goals_against", models.CharField(max_length=3)),
                ("goal_difference", models.CharField(max_length=3)),
                ("points", models.CharField(max_length=3)),
                ("form", models.CharField(max_length=5)),
                (
                    "league",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="tables",
                        to="home.league",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Results",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("team_1_name", models.CharField(max_length=75)),
                ("team_1_score", models.CharField(max_length=2)),
                ("team_2_name", models.CharField(max_length=75)),
                ("team_2_score", models.CharField(max_length=2)),
                ("date", models.DateField()),
                (
                    "league",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="results",
                        to="home.league",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Fixtures",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("team_1_name", models.CharField(max_length=75)),
                ("team_2_name", models.CharField(max_length=75)),
                ("date", models.DateField()),
                ("time", models.CharField(max_length=5)),
                (
                    "league",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="fixtures",
                        to="home.league",
                    ),
                ),
            ],
        ),
    ]
