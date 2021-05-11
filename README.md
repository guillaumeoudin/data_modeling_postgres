
# Project Description
This project is part of Udacity Data Engineering Nanodegree and was therefore lead for educational purposes.
Its main goals are :
- Applying data modeling with Postgres and defining a RDMS star schema for an analytic focus using the dimensional modeling paradigm (Facts vs Dimensions)
- Building an ETL pipeline using Python that transfers and process raw data from local directories into a Postgres database.

## Sparkify Database Project

This project creates a database for **Sparkify**, a fictional company offering music through its app. The purpose of the project is to create an ETL pipeline which extracts, transforms and loads semi-structured data from json files to structured data into a postgres database, enabling us to run analytics queries on the data.

## Data before modeling
The raw data consists of files located in 2 directories:
- the directory `data/log_data` of JSON logs on user activity on the app. Below is how the data is formatted in a json log file :
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
- the directory `data/song_data` which consists of JSON files containing metadata about the songs played in the app. Below is how the data is formatted in a json song file :
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

## DB Schema
The schema we will use is a star schema with **1 fact table** :

|songplays||
|-|-|
|songplay_id|SERIAL PRIMARY KEY| 
|start_time|BIGINT NOT NULL REFERENCES time (start_time)| 
|user_id|INT NOT NULL REFERENCES users (user_id)|
|level|VARCHAR|
|song_id|VARCHAR REFERENCES songs (song_id)|
|artist_id|VARCHAR REFERENCES artists (artist_id)|
|session_id|VARCHAR|
|location|VARCHAR| 
|user_agent|VARCHAR|


And **4 dimensions tables**:

|users||
|-|-|
|user_id|INT PRIMARY KEY| 
|first_name|VARCHAR|
|last_name|INT|
|gender|VARCHAR|
|level|VARCHAR|


|songs||
|-|-|
|song_id|VARCHAR PRIMARY KEY| 
|title|VARCHAR|
|artist_id|VARCHAR|
|year|INT|
|duration|NUMERIC|


|artists||
|-|-|
|artist_id|VARCHAR PRIMARY KEY| 
|artist_name|VARCHAR|
|artist_location|VARCHAR|
|artist_latitude|NUMERIC|
|artist_longitude|NUMERIC|


|time||
|-|-|
|start_time|BIGINT PRIMARY KEY| 
|hour|INT|
|day|INT|
|week|INT|
|month|INT|
|year|INT|
|weekday|INT|

This schema design will be used for easy analytics query.

# Quick Start

## Requirements
You need to have installed on your machine :
- python (3.8 or above)
- docker and docker-compose

## Project structure
```
data-modeling-postgres
├── README.md
├── requirements.txt
├── docker-compose.yml
├── database.env
├── data
│   ├── log_data
│   │   └── ...(logs)
│   └── song_data
│       └── ...(songs)
├── src
│   ├── notebooks
│   │   ├── etl.ipynb
│   │   └── test.ipynb
│   └── scripts
│       ├── create_tables.py
│       ├── etl.py
│       └── sql_queries.py
```

## Installation 
Run this command to clone the repository of the project
```bash
$ git clone https://github.com/guillaumeoudin/data_modeling_postgres
```
Then place yourself into the local repository
```bash
$ cd data_modeling_postgres
```
Setup a virtual envionement for the project and initialize it
```bash
$ python3 -m venv data-modeling-postgres
$ source data-modeling-postgres/bin/activate
```
Install needed dependencies
```
$ pip install -r requirements.txt
```

*Note : once finished working on the project, to close the virtual environment just run `deactivate`*

Next we will run a local postgres database with appropriate user/passwords credentials inside a docker container, and we will automatize this process using docker-compose *(see the `docker-compose.yml` file for reference)*.
```bash
$ docker-compose up -d 
```
Check the docker container is effectively running :
```
$ docker ps
```

## Instructions
Place yourself in the `src` folder
```bash
$ cd src/
``` 
Then execute the 2 scripts to respectively create the tables and then process the data from the files to the DB.
``` 
$ python scripts/create_tables.py
$ python scripts/etl.py
```      

## Results
We will run the test in the jupyter environement
```bash
$ jupyter notebook
```
Then navigate in Jupyter interface to `src/notebooks` and launch `test.ipynb` to run the different cells.


## Exemple queries

*What is the male/female repartition among our userbase ?*
```sql
SELECT gender, COUNT(gender)
FROM users
GROUP BY gender;
```
*Ouput:*

|gender|count|
|-|-|
|M|41|
|F|55|

<br>

*Where is located our userbase ?*
```sql
SELECT location, COUNT(location)
FROM songplays
GROUP BY location
ORDER BY COUNT(location) DESC;
```
*Ouput:*

|location|count|
|-|-|
|Atlanta-Sandy Springs-Roswell, GA|105|
|Waterloo-Cedar Falls, IA|86|
|Lansing-East Lansing, MI|75|
|...|...|

<br>

*Who are the users listening to the most songs ?*
```sql
SELECT u.first_name, u.last_name, u.user_id, COUNT(u.user_id)
FROM users as u
JOIN songplays as s
ON u.user_id=s.user_id
GROUP BY u.user_id
ORDER BY COUNT(u.user_id)
DESC;
```
*Output:*

|first_name|last_name|user_id|count|
|-|-|-|-|
|Jacqueline|Lynch|29|103|
|Aleena|Kirby|44|186|
|Kate|Harrell|97|75|
|...|...|...|...|

<br>

## Cleaning step
Running the following will stop and remove the container running the postgres database.
```bash
docker stop postgres-localdb-container && docker rm postgres-localdb-container
```



