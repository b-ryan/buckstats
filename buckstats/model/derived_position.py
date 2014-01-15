from buckstats.app import db


class DerivedPosition(db.Model):

    __tablename__ = 'derived_positions'

    id = db.Column(db.Integer, primary_key=True)
    position = db.Column(db.String, nullable=False)
    start_time = db.Column(db.DateTime, nullable=True)
    end_time = db.Column(db.DateTime, nullable=True)
