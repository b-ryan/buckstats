from buckstats.app import app, db
import buckstats.model as m
import flask
from flask.ext.restless import APIManager
import gspread
import config

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
