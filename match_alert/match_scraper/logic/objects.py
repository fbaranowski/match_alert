from dataclasses import dataclass
from datetime import datetime


@dataclass
class Team:
    name: str = "team_name"


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
class Fixture:
    team_1_name: str
    team_2_name: str
    date: datetime.date
    time: datetime.time


@dataclass
class Result:
    team_1_name: str
    team_1_score: int
    team_2_name: str
    team_2_score: int
    date: datetime.date
