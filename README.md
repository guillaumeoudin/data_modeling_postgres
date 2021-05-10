
# Project Description
This project was lead for educational purposes.
Its main goals are :
- Apply data modeling with Postgres
- Build an ETL pipeline using Python
- Define fact and dimension tables for a star schema for an analytic focus
- Write an ETL pipeline that transfers data from files located in 2 local directories into tables in Postgres using Python and SQL

# Sparkify Database Project
Sparkify decided to create a DB to store the data they've been collecting on songs and user activity on their new music streaming app. The goal is to enable the analytics team to run queries on the data, for instance to understand what songs users are listening to.
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

```
SELECT song_id
FROM songplays
JOIN  songs ON songplays.artist_id = songs.artist_id
ORDER BY

```

# (Optional) Run Postgres in Docker

Instructions below to run locally Postgres with Docker.

## First step : build Dockerfile

Create a file named 'Dockerfile' with the following content

```
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