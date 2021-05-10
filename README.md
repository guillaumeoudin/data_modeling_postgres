
# Project Description
This project was lead for educational purposes.
Its main goals are :
- Apply data modeling with Postgres
- Build an ETL pipeline using Python
- Define fact and dimension tables for a star schema for an analytic focus
- Write an ETL pipeline that transfers data from files located in 2 local directories into tables in Postgres using Python and SQL

# Sparkify Database Project

This project creates a postgres database `sparkifydb` for a fictional music app, *Sparkify*. The purpose of the database is to model song and log datasets (originaly stored in JSON format) with a star schema optimised for queries on song play analysis.

## The Data
Currently the data consists of:
- a directory of JSON logs on user activity on the app
- a directory of JSON metadata on the songs played in the app
## The Goal
ETL pipeline extract the data, applies the schema (star schema) and loads it in the Postgres DB.
## Database Schema
The schema used is a star schema. 

There is **1 fact table** :
- songplays

And **4 dimensions tables**:
- users
- songs
- artists
- time

This schema design is used to allow for easy query

# Example queries

```sql
SELECT song_id
FROM songplays
JOIN  songs ON songplays.artist_id = songs.artist_id
ORDER BY

```

# (Optional) Run Postgres in Docker

Instructions below to run locally Postgres with Docker.

## First step : build Dockerfile

Create a file named 'Dockerfile' with the following content

```docker
FROM library/postgres
ENV POSTGRES_USER student
ENV POSTGRES_PASSWORD student
ENV POSTGRES_DB studentdb
```

Then run this command in order to build from the newly created **Dockerfile** (make sure not to forget the **.** at the end of this command)
```
docker build -t postgres-localdb-image .
```

## Alternative step : retrieve image from docker hub

Execute to login then pull the image from docker hub
```
docker login docker.io
```
```
docker pull guillaumeoudin/postgres-localdb-image
```

## Final step : run the container from the build image
```
docker run -d --name postgres-localdb-container -p 5432:5432 postgres-localdb-image
```

## Cleaning step
Running the following will, in order, stop the container, remove the container, then remove the image.
```
docker stop postgres-localdb-container
docker rm postgres-localdb-container
docker rmi postgres-localdb-image
```


# Project: Data Modeling with Postgres

A startup named Sparkify wants to analyze user activities using their song and
user data. The current data is spread among several JSON files, making it hard
to query and analyze.

This project aims to create an ETL pipeline to load song and user data to a
Postgres database, making it easier to query and analyze data.

## Datasets

Data is currently collected for song and user activities, in two directories:
`data/log_data` and `data/song_data`, using JSON files.

### Song dataset format

```json
{
  "num_songs": 1,
  "artist_id": "ARGSJW91187B9B1D6B",
  "artist_latitude": 35.21962,
  "artist_longitude": -80.01955,
  "artist_location": "North Carolina",
  "artist_name": "JennyAnyKind",
  "song_id": "SOQHXMF12AB0182363",
  "title": "Young Boy Blues",
  "duration": 218.77506,
  "year": 0
}
```

### Log dataset format

```json
{
  "artist": "Survivor",
  "auth": "Logged In",
  "firstName": "Jayden",
  "gender": "M",
  "itemInSession": 0,
  "lastName": "Fox",
  "length": 245.36771,
  "level": "free",
  "location": "New Orleans-Metairie, LA",
  "method": "PUT",
  "page": "NextSong",
  "registration": 1541033612796,
  "sessionId": 100,
  "song": "Eye Of The Tiger",
  "status": 200,
  "ts": 1541110994796,
  "userAgent": "\"Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.143 Safari/537.36\"",
  "userId": "101"
}
```

## Schema

### Fact tables

#### Songplays

Records in log data associated with song plays i.e. records with `page` set to
`NextSong`.

|   Column    |            Type             | Nullable |
| ----------- | --------------------------- | -------- |
| songplay_id | integer                     | not null |
| start_time  | timestamp without time zone | not null |
| user_id     | integer                     | not null |
| level       | character varying           | not null |
| song_id     | character varying(18)       |          |
| artist_id   | character varying(18)       |          |
| session_id  | integer                     | not null |
| location    | character varying           | not null |
| user_agent  | character varying           | not null |

Primary key: songplay_id

### Dimension tables

#### Users

Users in the app.

|   Column   |       Type        | Nullable |
| ---------- | ----------------- | -------- |
| user_id    | integer           | not null |
| first_name | character varying | not null |
| last_name  | character varying | not null |
| gender     | character(1)      | not null |
| level      | character varying | not null |

Primary key: user_id

#### Songs

Songs in music database.

|  Column   |         Type          | Nullable |
| --------- | --------------------- | -------- |
| song_id   | character varying(18) | not null |
| title     | character varying     | not null |
| artist_id | character varying(18) | not null |
| year      | integer               | not null |
| duration  | double precision      | not null |

Primary key: song_id

#### Artists

Artists in music database.

|  Column   |         Type          | Nullable |
| --------- | --------------------- | -------- |
| artist_id | character varying(18) | not null |
| name      | character varying     | not null |
| location  | character varying     | not null |
| latitude  | double precision      |          |
| longitude | double precision      |          |

Primary key: artist_id

#### Time

Timestamps of records in songplays broken down into specific units.

|   Column   |            Type             | Nullable |
| ---------- | --------------------------- | -------- |
| start_time | timestamp without time zone | not null |
| hour       | integer                     | not null |
| day        | integer                     | not null |
| week       | integer                     | not null |
| month      | integer                     | not null |
| year       | integer                     | not null |
| weekday    | integer                     | not null |

## Build

Pre-requisites:

- Python 3
- pipenv
- pyenv (optional)
- PostgreSQL Database

To install project python dependencies, you should run:

``` sh
pipenv install
```

## Database

The database can be installed locally or ran using Docker, which is the
preferred method.

To use docker to run Postgres, you should run:

``` sh
docker run --net=host --name postgres -e POSTGRES_PASSWORD=your_password -d postgres
```

### Access and user setup

To initially access the database, you should run:

``` sh
psql -h localhost -U postgres
```

You should run the following commands under psql to setup user access to
Postgres and create the initial `sparkifydb` database:

``` sql
CREATE ROLE student WITH ENCRYPTED PASSWORD 'student';
ALTER ROLE student WITH LOGIN;
ALTER ROLE student CREATEDB;
CREATE DATABASE sparkifydb OWNER student;
```

## Running

To run the project locally, use pipenv to activate the virtual environment:

``` sh
pipenv shell
```

And run the scripts to create database tables:

``` sh
./create_tables.py
```

and populate data into tables:

``` sh
./etl.py
```

Data can be verified using the provided `test.ipynb` jupyter notebook:

``` sh
jupyter notebook
```