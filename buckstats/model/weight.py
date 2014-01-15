from buckstats.app import db


class Weight(db.Model):

    __tablename__ = 'weights'

    date = db.Column(db.Date, nullable=False, primary_key=True)
    weight = db.Column(db.Float, nullable=False)
    goal_weight = db.Column(db.Float)
    notes = db.Column(db.String(300))
