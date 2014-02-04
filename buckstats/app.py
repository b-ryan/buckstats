import flask
from flask.ext.sqlalchemy import SQLAlchemy
from config import log_handlers
import logging

app = flask.Flask(__name__, static_folder=None)

db_uri = 'postgres://stand:password@localhost/stand'
app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
db = SQLAlchemy(app)

app.logger.setLevel(logging.DEBUG)

for handler in log_handlers:
    app.logger.addHandler(handler)

# Initalize the routes here because the routes module depends
# on this module. It's a bit of a circular dependency, but it
# handles just fine.
import buckstats.routes
