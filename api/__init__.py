import os

from flask import Flask
from flask_mqtt import Mqtt
from flask_migrate import Migrate

from config import Config
from api.extensions import db
from api.models import device, sensor, measurements

mqtt_client = Mqtt()
migrate = Migrate()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    with app.app_context():
        db.create_all()
        db.session.commit()
        migrate.init_app(app, db)
        mqtt_client.init_app(app)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from api.mqtt.client import mqtt_bp
    app.register_blueprint(mqtt_bp)

    @app.route('/')
    def index():
        return "INDEX"

    return app
