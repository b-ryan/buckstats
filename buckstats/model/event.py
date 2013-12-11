from buckstats.app import db

class Event(db.Model):

    __tablename__ = 'events'

    id                = db.Column(db.Integer, primary_key=True)
    event             = db.Column(db.String, nullable=False)
    time              = db.Column(db.DateTime, nullable=False)
