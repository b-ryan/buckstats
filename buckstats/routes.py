from buckstats.app import app, db
import buckstats.model as m
import flask
from flask.ext.restless import APIManager
import gspread
import config
from stand_logic import event_created
import os

BUCKSTATS_TOKEN = os.environ['BUCKSTATS_TOKEN']


def auth_preprocessor(**kwargs):
    token = flask.request.headers.get('token')
    if token != BUCKSTATS_TOKEN:
        raise flask.abort(401)

# this will create routes at /api/
api = APIManager(app, flask_sqlalchemy_db=db)

api.create_api(
    m.Weight,
    methods=['GET'],
    results_per_page=None,
    allow_functions=True,
)


@app.route('/api/weights/refresh', methods=['POST'])
def refresh_weights():
    gc = gspread.login(config.gmail_user, config.gmail_pass)

    sh = gc.open('Weight')
    worksheet = sh.worksheet('Weight')

    m.Weight.query.delete()

    for value in worksheet.get_all_values()[1:]:
        weight = m.Weight(
            date=value[0],
            weight=float(value[2]),
            goal_weight=(float(value[1]) if value[1] != '' else None),
            notes=(value[3] if value[3] != '' else None),
        )
        db.session.add(weight)

    db.session.commit()

    return 'ok'


def events_postprocessor(result, **kwargs):
    event = db.session.query(m.Event)\
        .filter_by(id=result['id'])\
        .first()
    event_created(event)

api.create_api(
    m.Event,
    methods=['GET', 'POST'],
    results_per_page=None,
    preprocessors={
        'POST': [auth_preprocessor],
    },
    postprocessors={
        'POST': [events_postprocessor],
    },
)

api.create_api(
    m.DerivedPosition,
    methods=['GET'],
    results_per_page=None,
)
