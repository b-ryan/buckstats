#!/usr/bin/env python
import work_listener as w
import sys
import psycopg2

connection = psycopg2.connect(
    host='127.0.0.1',
    database='stand',
    user='stand',
    password='password',
)
cursor = connection.cursor()
cursor.execute('SELECT event, time FROM events ORDER BY time ASC')

for event, time in cursor:
    w.save((event, str(time),))
