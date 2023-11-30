#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 30 17:42:21 2023

@author: yii
"""
import sqlite3

conn = sqlite3.connect('joycastle.db')

c = conn.cursor()

c.execute("""
          SELECT count(eventid) from game_events;
          """)
          
          
print(c.fetchall())
conn.commit()
conn.close()