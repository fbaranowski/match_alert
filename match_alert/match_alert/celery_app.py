import os
from celery import Celery
from celery.schedules import crontab
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "match_alert.settings")
django.setup()

from match_scraper.scraper import DatabaseHandler  # noqa


queue_app = Celery(
    "scraping_queue", backend="redis://redis:6379/0", broker="redis://redis:6379/0"
)

queue_app.conf.beat_schedule = {
    "scrape-only-once-in-august": {
        "task": "match_alert.celery_app.scrape_teams",
        "schedule": crontab("0", "0", day_of_month="1", month_of_year="8"),
    },
    "scrape-results": {
        "task": "match_alert.celery_app.scrape_results",
        "schedule": 1800
    },
    "scrape-fixtures": {
        "task": "match_alert.celery_app.scrape_fixtures",
        "schedule": 3600
    },
    "scrape-tables": {
        "task": "match_alert.celery_app.scrape_tables",
        "schedule": 900
    },
}


@queue_app.task
def scrape_results():
    db_handler = DatabaseHandler()
    db_handler.fill_result_model()


@queue_app.task
def scrape_fixtures():
    db_handler = DatabaseHandler()
    db_handler.fill_fixture_model()


@queue_app.task
def scrape_tables():
    db_handler = DatabaseHandler()
    db_handler.fill_table_model()


@queue_app.task
def scrape_teams():
    db_handler = DatabaseHandler()
    db_handler.fill_team_model()
