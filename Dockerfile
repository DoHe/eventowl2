FROM python:3
ENV PYTHONUNBUFFERED 1
ENV PIP_NO_CACHE_DIR false
RUN mkdir /app
WORKDIR /app
COPY Pipfile ./
COPY Pipfile.lock ./
RUN pip3 install pipenv
RUN pipenv install --deploy --system
