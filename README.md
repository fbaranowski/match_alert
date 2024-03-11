# Match Alert
This project contains football leagues' tables, results and fixtures
as well as specific team's results and fixtures from included leagues.
It is also possible to create profile and add leagues/teams to favourites


## Tech Stack
- Python 3.11
- Django
- Pipenv
- Docker
- Selenium
- BeautifulSoup4
- Celery
- PostgreSQL
- Redis

## Installation
A step by step list of commands / guide that informs how to install
locally an instance of this project.

It is necessary to have Docker installed
on your local machine - get Docker Desktop [here](https://www.docker.com/products/docker-desktop/)

Using cmd, clone the repository from GitHub:

`git clone https://github.com/fbaranowski/match_alert`

Then start containers with :

`docker-compose up --build`

(teraz co wpisać w urla w przeglądarce)

(opisać wjazd do kontenera, wrzucenie modeli lig do db,
odpalenie ręczne celery, dopisanie short_name to teamów)
## Screenshots








## Running the tests
From master directory, use `cd match_alert` to get into project
directory, then once again use `cd match_alert` where `manage.py`
file exists.

Then run all the tests using two commands:

`python manage.py test home`

`python manage.py test users`

## Authors
Filip Baranowski – baranowski.filip04@gmail.com

You can find me here at: [Github](https://github.com/fbaranowski)
                         [LinkedIn](https://www.linkedin.com/in/filip-baranowski-7b46a3198/)
