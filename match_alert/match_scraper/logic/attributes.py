from datetime import date, datetime


class WebsiteAttributes:
    TABLE_CLASS_NAME = "LeagueTable_leagueTable__6QbXM"
    BUTTON_CLASS_NAME = "football-matches__show-more"
    FIXTURES_RESULTS_CONTAINER_CLASS = "football-matches__container"
    LEAGUE_CLASS_NAME = "football-matches__heading"
    # LEAGUE_CLASS_NAME = 'table__caption'
    TEAMS_LIST_CLASS = "dcr-12fqtb6"
    LEAGUE_CONTAINER_ID = {
        "premier_league": "container-premier-league",
        "la_liga": "container-la-liga",
        "bundesliga": "container-bundesliga",
        "serie_a": "container-serie-a",
        "ligue_1": "container-ligue-1",
    }


class RegexPatterns:
    DATE_REGEX = r"([A-z]+\s\d{1,}\s[A-z]+\s\d{4})"
    GAMES_REGEX = r"(\d{2}\D\d{2}\s.*?)(?=\s\d|$)"
    FORM_COLUMN_REGEX = r"\b(Won|Drew|Lost)\s*(\w)?"
    MATCH_TIME_REGEX = r"(\d{2}\D\d{2}\s)"
    FIXTURE_TEAMS_REGEX = r"\w+(?=\n)|\w+\s\w+(?=\n)"
    RESULT_TEAMS_REGEX = r"\D+\s\D+(?=\s)|\D+(?=\s)"


class UrlsParams:
    league_name_url = {
        "premier_league": "premierleague",
        "la_liga": "laligafootball",
        "bundesliga": "bundesligafootball",
        "serie_a": "serieafootball",
        "ligue_1": "ligue1football",
    }


class Validator:
    @staticmethod
    def date_validator(date_to_validate) -> bool:
        """
        Method which validates results' dates to scrape,
        so only current season results will be scraped
        It is necessary to consider two periods, because games are played in two years,
        e.g. in season 2023/24 games are played between August 2023 until May/June 2024
        """
        today = date.today()
        last_day_of_year = datetime(today.year, 12, 31).date()
        end_of_season_date = datetime(today.year, 7, 1).date()
        first_day_of_year = datetime(today.year, 1, 1).date()
        end_of_season_date_after_nye = datetime(today.year - 1, 7, 1).date()

        if last_day_of_year >= today > end_of_season_date > date_to_validate:
            return False
        if (
            end_of_season_date > today > first_day_of_year
            and date_to_validate < end_of_season_date_after_nye
        ):
            return False
        return True
