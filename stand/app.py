import flask
from flask.ext.sqlalchemy import SQLAlchemy

app = flask.Flask(
    __name__,
    static_folder='static',
    static_url_path='/static'
)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://stand:password@localhost/stand'
db = SQLAlchemy(app)
