from sqlalchemy import ForeignKey

from api.extensions import db


class DeviceType(db.Model):
    __tablename__ = 'device_type'
    id = db.Column(db.Integer, primary_key=True)
    device_type = db.Column(db.String(50))


class Device(db.Model):
    __tablename__ = 'device'
    id = db.Column(db.Integer, primary_key=True)
    device_type = db.Column(db.Integer, ForeignKey('device_type.id'))
    mac_address = db.Column(db.String(17))
    localization = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(100), nullable=False)
