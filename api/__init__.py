import os
from flask import Flask, render_template
from config import Config
from api.extensions import db, mqtt_client, migrate, login
from api.models import device, sensor, measurements, user


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    app.jinja_env.auto_reload = True
    app.config["TEMPLATES_AUTO_RELOAD"] = True

    db.init_app(app)

    with app.app_context():
        db.create_all()
        db.session.commit()
        migrate.init_app(app, db)
        login.init_app(app, db)
        mqtt_client.init_app(app)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from api.mqtt.client import mqtt_bp
    app.register_blueprint(mqtt_bp)

    from api.home.home import home_bp
    app.register_blueprint(home_bp)

    from api.auth.auth import auth_bp
    app.register_blueprint(auth_bp)

    @app.errorhandler(500)
    def internal_server_error(error):
        return render_template('500.html'), 500

    @app.errorhandler(404)
    def url_not_found(error):
        return render_template('404.html'), 404

    @app.errorhandler(403)
    def access_forbidden(error):
        return render_template('403.html'), 403

    return app
