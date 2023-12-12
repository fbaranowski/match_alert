from dataclasses import dataclass
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import StaleElementReferenceException
import re


@dataclass
class TableLabels:
    position: str | int = "#"
    team: str = "Team"
    played: str | int = "P"
    won: str | int = "W"
    drew: str | int = "D"
    lost: str | int = "L"
    goals_for: str | int = "GF"
    goals_against: str | int = "GA"
    goal_difference: str | int = "GD"
    points: str | int = "PTS"
    form: str = "Form"


@dataclass
class WebsiteAttributes:
    table_class_name = "LeagueTable_leagueTable__6QbXM"
    button_class_name = "football-matches__show-more"
    fixtures_results_container_class = "football-matches__container"


@dataclass
class RegexPatterns:
    date_regex = r"([A-z]+\s\d{1,}\s[A-z]+\s\d{4})"
    games_regex = r"(\d{2}\D\d{2}\s.*?)(?=\s\d|$)"


@dataclass
class TableLeagueNames:
    premier_league = "premier-league"
    la_liga = "primera-division"
    bundesliga = "bundesliga"
    serie_a = "serie-a"
    ligue_1 = "ligue-1"


@dataclass
class FixturesResultsParams:
    # better dictionaries or fields? Or maybe dict with 2 element lists?
    league_url = {
        "premier_league": "premierleague",
        "la_liga": "laligafootball",
        "bundesliga": "bundesligafootball",
        "serie_a": "serieafootball",
        "ligue_1": "ligue1football",
    }

    league_to_split = {
        "premier_league": "Premier League",
        "la_liga": "La Liga",
        "bundesliga": "Bundesliga",
        "serie_a": "Serie A",
        "ligue_1": "Ligue 1",
    }

    premier_league_url = "premierleague"
    la_liga_url = "laligafootball"
    bundesliga_url = "bundesligafootball"
    serie_a_url = "serieafootball"
    ligue_1_url = "ligue1football"

    premier_league_split = "Premier League"
    la_liga_split = "La Liga"
    bundesliga_split = "Bundesliga"
    serie_a_split = "Serie A"
    ligue_1_split = "Ligue 1"


class Scraper:
    @staticmethod
    def get_table(league_name: str) -> list:
        """
        Function which scrapes league tables
        url parameter should be 'https://talksport.com/football/<league_name>/table'
        """
        full_table = []
        response = requests.get(f"https://talksport.com/football/{league_name}/table")
        soup = BeautifulSoup(response.content, "html.parser")

        scraped_table = soup.find(
            "table", {"class": WebsiteAttributes.table_class_name}
        )

        for row in scraped_table.tbody.find_all("tr"):
            # team = []
            columns = row.find_all("td")
            # for column in columns:
            # team.append(column.text.strip())
            team = TableLabels(
                position=columns[0].text.strip(),
                team=columns[1].text.strip(),
                played=columns[2].text.strip(),
                won=columns[3].text.strip(),
                drew=columns[4].text.strip(),
                lost=columns[5].text.strip(),
                goal_difference=columns[6].text.strip(),
                points=columns[7].text.strip(),
                form=columns[8].text.strip(),
            )
            full_table.append(team)

        return full_table

    @staticmethod
    def get_results(url_league_name: str, league_name_for_split: str) -> list:
        """
        Function which scrapes league results from given url
        league_name argument is necessary for proper splitting scraped result into list
        """
        options = webdriver.FirefoxOptions()
        options.add_argument("-headless")
        driver = webdriver.Firefox(options=options)
        driver.get(f"https://www.theguardian.com/football/{url_league_name}/results")

        button = driver.find_element(By.CLASS_NAME, WebsiteAttributes.button_class_name)
        for i in range(2):
            button.click()

        scraped_results = driver.find_element(
            By.CLASS_NAME, WebsiteAttributes.fixtures_results_container_class
        ).text
        driver.close()

        raw_results = re.sub(r"\nFT", " ", scraped_results)
        raw_results = re.sub(r"\n", " ", raw_results)
        split_results = re.split(f"{league_name_for_split}", raw_results)

        final_results = []
        for result in split_results:
            days = re.split(r"\s\s", result)
            formatted_day = [day.strip() for day in days]
            final_results.append(formatted_day)

        final_results.pop(-1)
        return final_results

    @staticmethod
    def get_fixtures(url_league_name: str, league_name_for_split: str) -> list:
        """
        Function which scrapes league fixtures from given url
        league_name argument is necessary for proper splitting scraped result into list
        """
        options = webdriver.FirefoxOptions()
        options.add_argument("-headless")
        driver = webdriver.Firefox(options=options)
        driver.get(f"https://www.theguardian.com/football/{url_league_name}/fixtures")

        button = driver.find_element(By.CLASS_NAME, WebsiteAttributes.button_class_name)
        while button:
            try:
                button.click()
            except StaleElementReferenceException:
                break

        scraped_fixtures = driver.find_element(
            By.CLASS_NAME, WebsiteAttributes.fixtures_results_container_class
        ).text
        driver.close()

        raw_fixtures = re.sub(r"\n", " ", scraped_fixtures)
        split_fixtures = re.split(f"{league_name_for_split}", raw_fixtures)

        final_fixtures = []
        for fixture in split_fixtures:
            date_as_list = re.findall(RegexPatterns.date_regex, fixture)
            temp = [date for date in date_as_list]

            games = re.findall(RegexPatterns.games_regex, fixture)
            for game in games:
                temp.append(game.strip())
            final_fixtures.append(temp)

        final_fixtures.pop(-1)
        return final_fixtures


# class DatabaseHandler:
#     # Facade
#     def fill_db(self):
#         # scraping and getting data from Scraper class
#         # saving the data to DB

print(Scraper.get_table(TableLeagueNames.premier_league))
print(
    Scraper.get_results(
        FixturesResultsParams.league_url["premier_league"],
        FixturesResultsParams.league_to_split["premier_league"],
    )
)
print(
    Scraper.get_fixtures(
        FixturesResultsParams.league_url["premier_league"],
        FixturesResultsParams.league_to_split["premier_league"],
    )
)
