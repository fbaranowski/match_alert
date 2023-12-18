from dataclasses import dataclass
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import (
    StaleElementReferenceException,
    NoSuchElementException,
)
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
    FIXTURE_TEAMS_REGEX = r"[A-z]+(?=\n)|[A-z]+\s[A-z]+(?=\n)"
    RESULT_TEAMS_REGEX = r"[A-z]+\s[A-z]+(?=\s)|[A-z]+(?=\s)"


class UrlsParams:
    league_name_url = {
        "premier_league": "premierleague",
        "la_liga": "laligafootball",
        "bundesliga": "bundesligafootball",
        "serie_a": "serieafootball",
        "ligue_1": "ligue1football",
    }


class Scraper:
    @staticmethod
    def get_teams(league_container: str):
        response = requests.get("https://www.theguardian.com/football/teams")
        soup = BeautifulSoup(response.content, "html.parser")

        league = soup.find("div", {"id": league_container})
        teams = league.find_all("li", class_=WebsiteAttributes.TEAMS_LIST_CLASS)
        teams_list = []
        for team in teams:
            teams_list.append(team.text)
        return teams_list

    @staticmethod
    def get_table2(league_name: str) -> list:
        """
        Function which scrapes league tables
        url parameter should be 'https://theguardian.com/football/<league_name>/table'
        """
        full_table = []
        response = requests.get(
            f"https://www.theguardian.com/football/{league_name}/table"
        )
        soup = BeautifulSoup(response.content, "html.parser")

        scraped_table = soup.find("table", {"class": "table"})

        for row in scraped_table.tbody.find_all("tr"):
            columns = row.find_all("td")

            form_column = re.findall(RegexPatterns.FORM_COLUMN_REGEX, columns[10].text)
            form_words = [element[0][0] for element in form_column]
            form_first_letters = "".join(form_words)

            team = TableLabels(
                position=columns[0].text.strip(),
                team=columns[1].text.strip(),
                played=columns[2].text.strip(),
                won=columns[3].text.strip(),
                drew=columns[4].text.strip(),
                lost=columns[5].text.strip(),
                goals_for=columns[6].text.strip(),
                goals_against=columns[7].text.strip(),
                goal_difference=columns[8].text.strip(),
                points=columns[9].text.strip(),
                form=form_first_letters,
            )
            full_table.append(team)
        return full_table

    @staticmethod
    def get_results(url_league_name: str) -> list:
        """
        Function which scrapes league results from given url
        """
        options = webdriver.FirefoxOptions()
        options.add_argument("-headless")
        driver = webdriver.Firefox(options=options)
        driver.get(f"https://www.theguardian.com/football/{url_league_name}/results")

        button = driver.find_element(By.CLASS_NAME, WebsiteAttributes.BUTTON_CLASS_NAME)
        for i in range(2):
            button.click()

        league_name = driver.find_element(
            By.CLASS_NAME, WebsiteAttributes.LEAGUE_CLASS_NAME
        ).text

        scraped_results = driver.find_element(
            By.CLASS_NAME, WebsiteAttributes.FIXTURES_RESULTS_CONTAINER_CLASS
        ).text

        driver.close()

        raw_results = re.sub(r"\nFT", " ", scraped_results)
        raw_results = re.sub(r"\n", " ", raw_results)
        split_results = re.split(f"{league_name}", raw_results)
        split_results.pop(-1)

        final_results = []
        for result in split_results:
            days = re.split(r"\s\s", result)
            formatted_day = [day.strip() for day in days]

            date = formatted_day[0]

            for i in range(1, len(formatted_day)):
                teams = re.findall(RegexPatterns.RESULT_TEAMS_REGEX, formatted_day[i])
                goals = re.findall(r"\d", formatted_day[i])
                res_dict = {
                    "date": date,
                    "team1": teams[0],
                    "score1": goals[0],
                    "team2": teams[1],
                    "score2": goals[1],
                }
                final_results.append(res_dict)

        return final_results

    @staticmethod
    def get_fixtures(url_league_name: str) -> list:
        """
        Function which scrapes league fixtures from given url
        """
        options = webdriver.FirefoxOptions()
        options.add_argument("-headless")
        driver = webdriver.Firefox(options=options)
        driver.get(f"https://www.theguardian.com/football/{url_league_name}/fixtures")

        try:
            button = driver.find_element(
                By.CLASS_NAME, WebsiteAttributes.BUTTON_CLASS_NAME
            )
        except NoSuchElementException:
            button = None

        while button:
            try:
                button.click()
            except StaleElementReferenceException:
                break

        league_name = driver.find_element(
            By.CLASS_NAME, WebsiteAttributes.LEAGUE_CLASS_NAME
        ).text

        scraped_fixtures = driver.find_element(
            By.CLASS_NAME, WebsiteAttributes.FIXTURES_RESULTS_CONTAINER_CLASS
        ).text

        driver.close()

        raw_fixtures = re.sub(r"CET|CEST|GMT|BST", " ", scraped_fixtures)
        split_fixtures = re.split(f"{league_name}", raw_fixtures)
        split_fixtures.pop(-1)

        final_fixtures = []
        for fixture in split_fixtures:
            date_as_list = re.findall(RegexPatterns.DATE_REGEX, fixture)
            temp = [date for date in date_as_list]

            times = re.findall(RegexPatterns.MATCH_TIME_REGEX, fixture)
            teams = re.findall(RegexPatterns.FIXTURE_TEAMS_REGEX, fixture)

            team1, team2 = 0, 1
            for i in range(len(times)):
                games = [times[i], teams[team1], teams[team2]]
                temp.append(games)
                team1, team2 = team1 + 2, team2 + 2
            final_fixtures.append(temp)
        return final_fixtures


# class DatabaseHandler:
#     # Facade
#     def fill_db(self):
#         # scraping and getting data from Scraper class
#         # saving the data to DB

# print(Scraper.get_table(TableLeagueNames.PREMIER_LEAGUE))
print(Scraper.get_results(UrlsParams.league_name_url["serie_a"]))
# print(
#     Scraper.get_fixtures(
#         UrlsParams.league_name_url["premier_league"]
#     )
# )
# print(Scraper.get_table2(UrlsParams.league_name_url['premier_league']))
# print(Scraper.get_table2(UrlsParams.league_name_url['la_liga']))
# print(Scraper.get_table2(UrlsParams.league_name_url['bundesliga']))
# print(Scraper.get_table2(UrlsParams.league_name_url['serie_a']))
# print(Scraper.get_table2(UrlsParams.league_name_url['ligue_1']))
print(Scraper.get_teams(WebsiteAttributes.LEAGUE_CONTAINER_ID["premier_league"]))
