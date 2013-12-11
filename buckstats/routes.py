from buckstats.app import app, db
import buckstats.model as m
import flask
from flask.ext.restless import APIManager

# this will create routes at /api/
api = APIManager(app, flask_sqlalchemy_db=db)

api.create_api(
    m.Weight,
    methods=['GET'],
    results_per_page=None,
    allow_functions=True,
)
