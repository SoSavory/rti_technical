FROM python:3-slim
# need these for psycopg2
RUN apt-get update && apt-get install -y libpq-dev gcc
RUN pip install --upgrade pip
RUN pip install psycopg2
RUN pip install pandas

COPY ./import_census.py /import_census.py
