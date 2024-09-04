import sqlalchemy.exc
from flask import Blueprint

from api.extensions import db
from api.extensions import mqtt_client

from api.models import device, sensor, measurements
import json

mqtt_bp = Blueprint('mqtt_bp', __name__, url_prefix='/mqtt_bp')


@mqtt_client.on_connect()
def handle_connect(client, userdata, flags, rc):
    print("rc: " + str(rc))
    if rc == 0:
        print('Connected successfully')
        mqtt_client.subscribe(mqtt_client.app.config.get('MQTT_TOPIC'))
    else:
        print('Bad connection. Code:', rc)


@mqtt_client.on_message()
def handle_mqtt_message(client, userdata, message):
    data = dict(
        topic=message.topic,
        payload=message.payload.decode()
    )

    #print('Received message on topic: {topic} with payload: {payload}'.format(**data))
    parse_message(message.payload)


def parse_message(payload):
    try:
        payload_dict = json.loads(payload)
        mac_address = payload_dict['d']
        measurements_list = payload_dict['m']

        for measurement_dict in measurements_list:
            sensor_type = measurement_dict['ty']
            measurement_date = measurement_dict['dt']

            with (mqtt_client.app.app_context()):
                try:
                    q = db.session.query(sensor.Sensor, sensor.SensorType, device.Device
                                         ).join(sensor.SensorType
                                                ).join(device.Device
                                                       ).filter(sensor.SensorType.sensor_type == sensor_type
                                                                ).filter(device.Device.mac_address == mac_address
                                                                         ).one()
                    sensor_id = q[0].id

                    temp = measurements.Temperature(sensor_id=sensor_id,
                                                    date=measurement_date,
                                                    value=measurement_dict['t'])
                    hum = measurements.Humidity(sensor_id=sensor_id,
                                                date=measurement_date,
                                                value=measurement_dict['h'])
                    db.session.add_all([temp, hum])
                    db.session.commit()
                except sqlalchemy.exc.NoResultFound:
                    pass
    except (json.decoder.JSONDecodeError, UnboundLocalError) as e:
        pass




