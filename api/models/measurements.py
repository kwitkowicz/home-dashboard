from sqlalchemy import ForeignKey

from api.extensions import db


class Temperature(db.Model):
    __table_name__='temperature'
    sensor_id = db.Column(db.Integer, ForeignKey('sensor.id'))
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime)
    value = db.Column(db.Float)

class Humidity(db.Model):
    __table_name__ = 'humidity'
    sensor_id = db.Column(db.Integer, ForeignKey('sensor.id'))
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime)
    value = db.Column(db.Float)