
# Project Description
This project was lead for educational purposes.
Its main goals are :
- Apply data modeling with Postgres
- Build an ETL pipeline using Python
- Define fact and dimension tables for a star schema for an analytic focus
- Write an ETL pipeline that transfers data from files located in 2 local directories into tables in Postgres using Python and SQL

# Sparkify Database Project

This project creates a postgres database `sparkifydb` for a fictional music app, *Sparkify*. The purpose of the project is to create an ETL pipeline which loads song and user data from json files to the database, enabling us to run analytics queries on the data

# Quick Start


We will need to run a local postgres DB. The easiest way to achieve that is with Docker. You will first need to [install Docker from their website](https://www.docker.com) then either build the image with the provided Dockerfile or pull [ my image from Docker Hub](https://hub.docker.com/r/guillaumeoudin/postgres-localdb-image).

### Option #1 : Building from Dockerfile

Create the Dockerfile or use the one provided
```docker
FROM library/postgres
ENV POSTGRES_USER student
ENV POSTGRES_PASSWORD student
ENV POSTGRES_DB studentdb
```
Then build
```
docker build -t postgres-localdb-image .
```

### Option #2 : Building from Dockerfile

Run the following 
```bash
$ git clone https://github.com/guillaumeoudin/data_modeling_postgres
$ cd data_modeling_postgres
$ python3 create_tables.py
$ python3 etl.py
```



## The Data
Currently the data consists of:
- A directory of JSON logs on user activity on the app. Below is how the data is formatted in a json log file :
```json
{
    "artist":"Des'ree",
    "auth":"Logged In",
    "firstName":"Kaylee",
    "gender":"F",
    "itemInSession":1,
    "lastName":"Summers",
    "length":246.30812,
    "level":"free",
    "location":"Phoenix-Mesa-Scottsdale, AZ",
    "method":"PUT",
    "page":"NextSong",
    "registration":1540344794796.0,
    "sessionId":139,
    "song":"You Gotta Be",
    "status":200,
    "ts":1541106106796,
    "userAgent":"\"Mozilla\/5.0 (Windows NT 6.1; WOW64
    AppleWebKit\/537.36 (KHTML, like Gecko) Chrome\/35.0
    1916.153 Safari\/537.36\"",
    "userId":"8"
}
```
- a directory of JSON metadata on the songs played in the app. Below is how the data is formatted in a json song file :
```json
{
    "num_songs": 1,
    "artist_id": "ARD7TVE1187B99BFB1",
    "artist_latitude": null,
    "artist_longitude": null,
    "artist_location": "California - LA",
    "artist_name": "Casual",
    "song_id": "SOMZWCG12A8C13C480",
    "title": "I Didn't Mean To",
    "duration": 218.93179,
    "year": 0
}
```
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



### Log dataset format



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