
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

###### This is an <h6> tag
test

State and justify your database schema design and ETL pipeline.
[Optional] Provide example queries and results for song play analysis.

what songs users are listening to
```
"""
SELECT song_id
FROM songplays
JOIN  songs ON songplays.artist_id = songs.artist_id
ORDER BY

```