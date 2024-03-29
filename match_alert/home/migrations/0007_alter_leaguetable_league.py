# Generated by Django 4.2.7 on 2024-01-08 17:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("home", "0006_rename_table_leaguetable"),
    ]

    operations = [
        migrations.AlterField(
            model_name="leaguetable",
            name="league",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="table",
                to="home.league",
            ),
        ),
    ]
