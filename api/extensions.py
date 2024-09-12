from flask_mqtt import Mqtt
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
mqtt_client = Mqtt(connect_async=True)

login.login_view = 'auth_bp.login'
login.login_message = ('Please log in to access this page.')
login.login_message_category = 'alert-secondary'
