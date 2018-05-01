FROM python:3
ENV PYTHONUNBUFFERED 1
ENV PIP_NO_CACHE_DIR false
RUN mkdir /app
WORKDIR /app
RUN pip3 install pipenv
COPY Pipfile ./
COPY Pipfile.lock ./
RUN pipenv install --deploy --system
