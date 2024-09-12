from flask_login import UserMixin
from api.extensions import db, login


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    username = db.Column(db.String(100))
    password = db.Column(db.String(256))


@login.user_loader
def load_user(id):
    return db.session.get(User, int(id))
