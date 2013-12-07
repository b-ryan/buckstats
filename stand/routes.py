from stand.app import app, db
import stand.model as m
import flask
from flask.ext.restless import APIManager

@app.route('/')
def index():
    return app.send_static_file('html/index.html')
