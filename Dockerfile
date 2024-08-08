FROM python:3.11-alpine
WORKDIR src/
ENV SECRET_KEY=${SECRET_KEY}
ENV NAME=${POSTGRES_DB}
ENV USER=${POSTGRES_USER}
ENV PASSWORD=${POSTGRES_PASSWORD}
ENV HOST=${POSTGRES_HOST}
ENV PORT=${POSTGRES_PORT}
COPY Pipfile Pipfile.lock ./
RUN python -m pip install --upgrade pip
RUN pip install --no-cache-dir pipenv && pipenv install --dev --system --deploy
COPY match_alert/ ./
