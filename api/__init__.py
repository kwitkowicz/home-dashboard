import os

from flask import Flask
from flask_mqtt import Mqtt

from config import Config

mqtt_client = Mqtt()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

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
