FROM python:3.9

WORKDIR /usr/src/lukuvinkkikirjasto

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV FLASK_ENV development
ENV FLASK_APP src/app.py
ENV POETRY_HOME=/usr

# Install Poetry for managing Python packages
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/install-poetry.py | python3 -
RUN poetry --version

# Change to run as non root
# RUN adduser lukuvinkkikirjasto
# USER lukuvinkkikirjasto

# copy install files for installing dependencies
COPY pyproject.toml poetry.lock /usr/src/lukuvinkkikirjasto/

# install python dependencies
RUN poetry install --no-interaction

EXPOSE 5000

COPY . /usr/src/lukuvinkkikirjasto

CMD ["poetry","run","invoke","start"]