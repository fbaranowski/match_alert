from celery import Celery
from celery.schedules import crontab
from django.conf import settings
from match_scraper.scraper import DatabaseHandler

settings.configure()
queue_app = Celery(
    "scraping_queue", backend="redis://redis:6379/0", broker="redis://redis:6379/0"
)

queue_app.conf.beat_schedule = {
    "scrape-every-hour": {
        "task": "tasks.scrape_fixtures_results_tables",
        "schedule": 3600,
    },
    "scrape-only-once-in-august": {
        "task": "tasks.scrape_teams",
        "schedule": crontab("0", "0", day_of_month="1", month_of_year="8"),
    },
}


@queue_app.task
def scrape_fixtures_results_tables():
    db_handler = DatabaseHandler()
    db_handler.fill_table_model()
    db_handler.fill_fixture_model()
    db_handler.fill_result_model()


@queue_app.task
def scrape_teams():
    db_handler = DatabaseHandler()
    db_handler.fill_team_model()