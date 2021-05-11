import os
import glob
import psycopg2
import pandas as pd
from sql_queries import *


def process_song_file(cur, filepath):
    
    """
    This procedure processes a song file whose filepath has been provided as an arugment.
    It extracts the song information in order to store it into the songs table.
    Then it extracts the artist information in order to store it into the artists table.

    INPUTS: 
    * cur the cursor variable
    * filepath the file path to the song file
    """

    # open song file
    df = pd.read_json(filepath, typ='series')
    df = df.to_frame().T

    # insert song record
    song_data = df.loc[0,['song_id', 'title', 'artist_id', 'year', 'duration']]
    song_data = song_data.values.tolist()
    cur.execute(song_table_insert, song_data)
    
    # insert artist record
    artist_data = df.loc[0,['artist_id', 'artist_name', 'artist_location', 'artist_latitude', 'artist_longitude']]
    artist_data = artist_data.values.tolist()
    cur.execute(artist_table_insert, artist_data)


def process_log_file(cur, filepath):

    """
    This function processes a log file whose filepath has been provided as an arugment.
    It extracts the log information in order to store it into the time table.
    Then it extracts the user information in order to store it into the users table.
    Finally it queries the songs and artists tables to retrieve respective IDs and inserts
    the data from time and users tables into the songplay table.

    INPUTS: 
    * cur the cursor variable
    * filepath the file path to the log file
    """

    
    # open log file
    df = pd.read_json(filepath, lines=True)

    # filter by NextSong action
    df = df[df.page == 'NextSong']

    # convert timestamp column to datetime
    t = pd.to_datetime(df['ts'], unit='ms')
    
    # insert time data records
    time_data = []
    time_data.extend((df['ts'],
                      t.dt.hour,
                      t.dt.day,
                      t.dt.isocalendar().week,
                      t.dt.month,
                      t.dt.year,
                      t.dt.weekday))
    
    #creating the list of column labels
    column_labels = ['timestamp','hour', 'day', 'week', 'month', 'year', 'weekday']
    
    #creating dictionnary to load data into a pandas DataFrame
    time_dict = {}
    for k, v in zip(column_labels, time_data):
        time_dict[k] = v
    
    #loading data into DataFrame
    time_df = pd.DataFrame(time_dict)

    for i, row in time_df.iterrows():
        cur.execute(time_table_insert, list(row))

    # load user table
    user_df = df[['userId', 'firstName', 'lastName', 'gender', 'level']]
    user_df.columns = ['user_id', 'first_name', 'last_name', 'gender', 'level']
    user_df = user_df.drop_duplicates() 

    # insert user records
    for i, row in user_df.iterrows():
        cur.execute(user_table_insert, row)

    # insert songplay records
    for index, row in df.iterrows():
        
        # get songid and artistid from song and artist tables
        cur.execute(song_select, (row.song, row.artist, row.length))
        results = cur.fetchone()
        
        if results:
            songid, artistid = results
        else:
            songid, artistid = None, None

        # insert songplay record
        songplay_data = (row.ts,
                         row.userId,
                         row.level,
                         songid,
                         artistid,
                         row.sessionId,
                         row.location,
                         row.userAgent)
   
        cur.execute(songplay_table_insert, songplay_data)


def process_data(cur, conn, filepath, func):

    """
    This function first look for json files in the given path, stores the paths into a list
    and prints the total number of files.
    Then it iterates over the paths in the list and applies the function passed as argument
    to each of the files.
    Finally it commits the transaction to the database.
    
    INPUTS: 
    * cur the cursor variable
    * conn the connection variable
    * filepath the file path to the log file  
    * func the function we want to process the files with

    """


    # get all files matching extension from directory
    all_files = []
    for root, dirs, files in os.walk(filepath):
        files = glob.glob(os.path.join(root,'*.json'))
        for f in files :
            all_files.append(os.path.abspath(f))

    # get total number of files found
    num_files = len(all_files)
    print(f'\n{num_files} files found in {all_files}\n')

    # iterate over files and process
    for i, datafile in enumerate(all_files, 1):
        func(cur, datafile)
        conn.commit()
        print(f'{i}/{num_files} files processed.')


def main():

    """
    This function is connecting to the local database and setting up a cursor for us to use.
    It then calls the process_data function to launch the ETL pipeline.
    """

    conn = psycopg2.connect("host=127.0.0.1 dbname=sparkifydb user=student password=student")
    cur = conn.cursor()

    process_data(cur, conn, filepath='../data/song_data', func=process_song_file)
    process_data(cur, conn, filepath='../data/log_data', func=process_log_file)

    conn.close()


if __name__ == "__main__":
    main()