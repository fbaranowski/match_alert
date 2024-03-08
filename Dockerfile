FROM python:3.11-alpine
WORKDIR src/
COPY Pipfile Pipfile.lock ./
RUN python -m pip install --upgrade pip
RUN pip install --no-cache-dir pipenv && pipenv install --dev --system --deploy
COPY match_alert/ ./
CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]
