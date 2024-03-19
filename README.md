# Match Alert
This project contains football leagues' tables, results and fixtures
as well as specific team's results and fixtures from included leagues.
It is also possible to create profile and add leagues/teams to favourites.

The application scrapes all the required information periodically using
Celery queues and saves them in the database.


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
A step-by-step list of commands/guide that informs how to install
locally an instance of this project.

It is necessary to have Docker installed
on your local machine - get Docker Desktop [here](https://www.docker.com/products/docker-desktop/)

Using cmd, clone the repository from GitHub:

`git clone https://github.com/fbaranowski/match_alert`

Then start containers with :

`docker-compose up --build`

And now just open browser and go to `http://localhost:8000`

Sometimes it may be necessary to run celery task manually.
In order to do that, containers must be running.
Then, it is necessary to enter the container with Django app using:

`docker exec -it <web-container-name> sh`

Next, enter Django shell, import celery tasks and run them:

`python manage.py shell`

`from match_alert.celery_app import scrape_fixtures_results_tables, scrape_teams`

`scrape_fixtures_results_tables.apply()`

`scrape_teams.apply()`


## Screenshots
![Screenshot of table](./screenshots/table.jpg?raw=true)

![Screenshot of results](./screenshots/results.jpg?raw=true)

![Screenshot of fixtures](./screenshots/fixtures.jpg?raw=true)


## Running the tests
From master directory, use `cd match_alert` to get into project
directory, then once again use `cd match_alert` where `manage.py`
file exists.

Then run all the tests using two commands:

`python manage.py test home`

`python manage.py test users`


## Authors
Filip Baranowski – baranowski.filip04@gmail.com

You can find me here at:

[Github](https://github.com/fbaranowski)

[LinkedIn](https://www.linkedin.com/in/filip-baranowski-7b46a3198/)
