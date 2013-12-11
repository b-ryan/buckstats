import flask
from flask.ext.sqlalchemy import SQLAlchemy

app = flask.Flask(__name__, static_folder=None)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://stand:password@localhost/stand'
db = SQLAlchemy(app)

# Initalize the routes here because the routes module depends
# on this module. It's a bit of a circular dependency, but it
# handles just fine.
import buckstats.routes
