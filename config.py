import os
import ssl

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY')
    MQTT_BROKER_URL = os.environ.get('MQTT_BROKER_URL')
    MQTT_BROKER_PORT = int(os.environ.get('MQTT_BROKER_PORT'))
    MQTT_USERNAME = os.environ.get('MQTT_USERNAME')
    MQTT_PASSWORD = os.environ.get('MQTT_PASSWORD')
    MQTT_KEEPALIVE = int(os.environ.get('MQTT_KEEPALIVE'))
    MQTT_TLS_ENABLED = os.environ.get('MQTT_TLS_ENABLED')
    MQTT_TOPIC = os.environ.get('MQTT_TOPIC')
    """This server-side CA is public available on emqx website"""
    MQTT_TLS_CA_CERTS = 'api/mqtt/certs/emqxsl-ca.crt'
    MQTT_TLS_VERSION = ssl.PROTOCOL_TLSv1_2