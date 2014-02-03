from buckstats.app import db


class ApiKey(db.Model):

    __tablename__ = 'api_keys'

    id = db.Column(db.Integer, primary_key=True)
    api_key = db.Column(db.String, nullable=False)
