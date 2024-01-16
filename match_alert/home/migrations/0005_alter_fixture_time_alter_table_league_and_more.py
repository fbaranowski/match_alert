# Generated by Django 4.2.7 on 2023-12-31 13:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("home", "0004_team_table_result_fixture"),
    ]

    operations = [
        migrations.AlterField(
            model_name="fixture",
            name="time",
            field=models.TimeField(),
        ),
        migrations.AlterField(
            model_name="table",
            name="league",
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="table",
                to="home.league",
            ),
        ),
        migrations.AlterField(
            model_name="team",
            name="league",
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="teams",
                to="home.league",
            ),
        ),
    ]