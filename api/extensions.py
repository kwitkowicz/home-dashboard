from flask_mqtt import Mqtt
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
mqtt_client = Mqtt(connect_async=True)