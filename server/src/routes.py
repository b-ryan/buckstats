#!/usr/bin/env python
import os, sys
import bottle
import psycopg2

DIR = os.path.abspath(os.path.dirname(__file__))
PUBLIC = os.path.join(DIR, '../public')

connection = psycopg2.connect(
    host='127.0.0.1',
    database='stand',
    user='stand',
    password='password',
)

@bottle.get('/')
def index():
    return bottle.static_file('html/index.html', PUBLIC)

@bottle.get('/public/<filename:path>')
def public(filename):
    return bottle.static_file(filename, PUBLIC)

bottle.run(port=8080)
