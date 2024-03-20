import re
import requests
from datetime import datetime
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import (
    StaleElementReferenceException,
    NoSuchElementException,
    ElementClickInterceptedException,
)
from selenium.webdriver.firefox.options import Options
from match_scraper.logic.attributes import WebsiteAttributes, RegexPatterns, Validator
from match_scraper.logic.objects import Team, TableLabels, Fixture, Result


class Scraper:
    @staticmethod
    def get_teams(league_container: str):
        response = requests.get("https://www.theguardian.com/football/teams")
        soup = BeautifulSoup(response.content, "html.parser")

        league = soup.find("div", {"id": league_container})
        teams = league.find_all("li", class_=WebsiteAttributes.TEAMS_LIST_CLASS)
        teams_list = []
        for team in teams:
            team_obj = Team(name=team.text)
            teams_list.append(team_obj)
        return teams_list

    @staticmethod
    def get_table(league_name: str) -> list:
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
                position=int(columns[0].text.strip()),
                team=columns[1].text.strip(),
                played=int(columns[2].text.strip()),
                won=int(columns[3].text.strip()),
                drew=int(columns[4].text.strip()),
                lost=int(columns[5].text.strip()),
                goals_for=int(columns[6].text.strip()),
                goals_against=int(columns[7].text.strip()),
                goal_difference=int(columns[8].text.strip()),
                points=int(columns[9].text.strip()),
                form=form_first_letters,
            )
            full_table.append(team)
        return full_table

    @staticmethod
    def get_results(url_league_name: str) -> list:
        """
        Function which scrapes league results from given url
        """
        driver_path = "http://firefox:4444"
        options = Options()
        options.add_argument("-headless")
        driver = webdriver.Remote(command_executor=driver_path, options=options)
        driver.get(f"https://www.theguardian.com/football/{url_league_name}/results")

        try:
            button = driver.find_element(
                By.CLASS_NAME, WebsiteAttributes.BUTTON_CLASS_NAME
            )
        except NoSuchElementException:
            button = None

        while button:
            try:
                button.click()
            except ElementClickInterceptedException:
                break

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
            date = datetime.strptime(date, "%A " "%d " "%B " "%Y").date()

            if not Validator.date_validator(date_to_validate=date):
                break

            for i in range(1, len(formatted_day)):
                teams = re.findall(RegexPatterns.RESULT_TEAMS_REGEX, formatted_day[i])
                goals = re.findall(r"\d", formatted_day[i])

                result = Result(
                    team_1_name=teams[0].strip(),
                    team_1_score=int(goals[0]),
                    team_2_name=teams[1].strip(),
                    team_2_score=int(goals[1]),
                    date=date,
                )
                final_results.append(result)

        return final_results

    @staticmethod
    def get_fixtures(url_league_name: str) -> list:
        """
        Function which scrapes league fixtures from given url
        """
        driver_path = "http://firefox:4444"
        options = Options()
        options.add_argument("-headless")
        driver = webdriver.Remote(command_executor=driver_path, options=options)
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
            teams.pop(0)

            team1, team2 = 0, 1
            for i in range(len(times)):
                date = datetime.strptime(temp[0], "%A " "%d " "%B " "%Y").date()
                time = datetime.strptime(times[i].strip(), "%H:%M").time()
                game = Fixture(
                    team_1_name=teams[team1],
                    team_2_name=teams[team2],
                    date=date,
                    time=time,
                )
                team1, team2 = team1 + 2, team2 + 2
                final_fixtures.append(game)
        return final_fixtures
