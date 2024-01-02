class WebsiteAttributes:
    TABLE_CLASS_NAME = "LeagueTable_leagueTable__6QbXM"
    BUTTON_CLASS_NAME = "football-matches__show-more"
    FIXTURES_RESULTS_CONTAINER_CLASS = "football-matches__container"
    LEAGUE_CLASS_NAME = "football-matches__heading"
    TEAMS_LIST_CLASS = "dcr-12fqtb6"
    LEAGUE_CONTAINER_ID = {
        "premier_league": "container-premier-league",
        "la_liga": "container-la-liga",
        "bundesliga": "container-bundesliga",
        "serie_a": "container-serie-a",
        "ligue_1": "container-la-liga",
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
