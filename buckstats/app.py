import flask
from flask.ext.sqlalchemy import SQLAlchemy

app = flask.Flask(__name__, static_folder=None)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://stand:password@localhost/stand'
db = SQLAlchemy(app)
