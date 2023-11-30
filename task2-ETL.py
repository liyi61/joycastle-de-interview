#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 29 18:30:10 2023

@author: yii
"""

import sqlite3
import pandas as pd

#read data from the previously downloaded csv file
df_events = pd.read_csv("game_events.csv")

#check data info
print(df_events.info())

print(df_events['EventTimestamp'])

#get a preview of the data
print(df_events.head(20))

#convert the data type of 'EventTimestamp' from object to datatime
df_events['EventTimestamp'] = pd.to_datetime(df_events['EventTimestamp'],format='mixed')
print("Converted 'EventTimestamp' from object to datetime")

#set an index for the dataframe
df_events = df_events.set_index('EventID')
print("set 'EventID' as index")

#connect to sqlite and create a new database
conn = sqlite3.connect('joycastle.db')

#write the dataframe into a temp table in the sqlite database
#sqlite can't be modified (change columns datatype, add primary key etc.) after they have been created
#so we will create a new table with the right requirements and copy the data into it, then drop the temp table.
table_name = "temp"
df_events.to_sql(table_name, conn, if_exists='replace') 

#start a transaction manually
conn.execute('BEGIN')

try:
    
    #create a cursor
    c = conn.cursor()
    
    #Create table game_events (this will be the destination of this ETL process)
    c.execute("""
              CREATE TABLE `game_events` (
              `EventID` text PRIMARY KEY,
              `PlayerID` text,
              `EventTimestamp` datetime,
              `EventType` text,
              `EventDetails` text,
              `DeviceType` text,
              `Location` text
            ) ;
              """)
              
    #copy data from temp to game_events          
    c.execute("""
              INSERT INTO game_events (EventID, PlayerID, EventTimestamp,EventType,EventDetails,DeviceType,Location)
              SELECT EventID, PlayerID, EventTimestamp,EventType,EventDetails,DeviceType,Location
              FROM temp
              """)
              
    #drop the temp table          
    c.execute("""
              DROP TABLE temp;
              """)
              
    #check table info
    c.execute("""
              PRAGMA table_info(game_events)
              
              """)
              
    #commit the changes
    conn.commit()
              
except Exception as e:
    #an error occurred, rollback the changes
    conn.rollback()
    print(f"Error: {e}")
               
finally:
    #close the cursor and connection
    conn.close

print("Data loaded into SQLite db... db = joycastle... table = game_events")
    
    
    
    