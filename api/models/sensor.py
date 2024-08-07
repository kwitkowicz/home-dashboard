from sqlalchemy import ForeignKey

from api.extensions import db

class SensorType(db.Model):
    __table_name__='sensor_type'
    id = db.Column(db.Integer, primary_key=True)
    sensor_type = db.Column(db.String(50))

class Sensor(db.Model):
    __table_name__='sensor'
    id = db.Column(db.Integer, primary_key=True)
    sensor_type = db.Column(db.Integer, ForeignKey('sensor_type.id'))
    device_id = db.Column(db.Integer, ForeignKey('device.id'))