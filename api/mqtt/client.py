from flask import Blueprint

from api import mqtt_client

mqtt_bp = Blueprint('mqtt_bp', __name__, url_prefix='/mqtt_bp')


@mqtt_client.on_connect()
def handle_connect(client, userdata, flags, rc):
    print("rc: " + str(rc))
    if rc == 0:
        print('Connected successfully')
        mqtt_client.subscribe(mqtt_client.app.config.get('MQTT_TOPIC'))  # subscribe topic
    else:
        print('Bad connection. Code:', rc)


@mqtt_client.on_message()
def handle_mqtt_message(client, userdata, message):
    data = dict(
        topic=message.topic,
        payload=message.payload.decode()
    )
    print('Received message on topic: {topic} with payload: {payload}'.format(**data))
