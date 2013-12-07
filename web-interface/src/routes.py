#!/usr/bin/env python
import os, sys
import bottle
import psycopg2
import json
import datetime

DIR = os.path.abspath(os.path.dirname(__file__))
PUBLIC = os.path.join(DIR, '../public')

class CustomEncoder(json.JSONEncoder):
    
    def default(self, obj):
        if hasattr(obj, '__dict__'):
            return obj.__dict__
        return str(obj)

class Event:

    def __init__(self, row):
        self.id         = row[0]
        self.event      = row[1]
        self.start_time = row[2]
        self.end_time   = row[3]

    def stop(self):
        self.end_time = datetime.datetime.now()

connection = psycopg2.connect(
    host='127.0.0.1',
    database='stand',
    user='stand',
    password='password',
)
cursor = connection.cursor()

def get_latest():
    cursor.execute('''
        SELECT id, event, start_time, end_time
        FROM events
        ORDER BY id DESC
        LIMIT 1
        '''
    )
    latest = cursor.fetchone()
    return Event(latest) if latest else None

def save(event):
    cursor.execute('''
        REPLACE into events (id, event, start_time, end_time)
        VALUES (?, ?, ?, ?)
        ''',
        (event.id, event.event, event.start_time, event.end_time,)
    )
    connection.commit()

@bottle.get('/')
def index():
    return bottle.static_file('html/index.html', PUBLIC)

@bottle.get('/public/<filename:path>')
def public(filename):
    return bottle.static_file(filename, PUBLIC)

@bottle.get('/events')
def events():
    cursor.execute('''
        SELECT id, event, start_time, end_time
        FROM events
        ORDER BY id DESC
    ''')
    events = map(Event, cursor.fetchall())
    return json.dumps(events, cls=CustomEncoder)

@bottle.post('/stop')
def stop():
    latest = get_latest()
    if latest and latest.end_time is None:
        latest.stop()
        save(latest)
    return json.dumps(latest, cls=CustomEncoder)

bottle.run(port=8080, reloader=True)
