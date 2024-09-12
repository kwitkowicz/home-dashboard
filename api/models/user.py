from flask_login import UserMixin, AnonymousUserMixin
from api.extensions import db, login


class Permission:
    DEFAULT = 0x01
    USER = 0x08
    ADMIN = 0x80


class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    index = db.Column(db.String(64))
    default = db.Column(db.Boolean, default=False, index=True)
    permissions = db.Column(db.Integer)
    users = db.relationship('User', backref='role', lazy='dynamic')

    @staticmethod
    def insert_roles():
        roles = {
            'Default': (0x01, 'default', True),
            'User': (0x0f, 'user', False),
            'Administrator': (
                0xff,
                'admin',
                False  # grants all permissions
            )
        }
        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role = Role(name=r)
            role.permissions = roles[r][0]
            role.index = roles[r][1]
            role.default = roles[r][2]
            db.session.add(role)
        db.session.commit()


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    username = db.Column(db.String(100))
    password = db.Column(db.String(256))
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))

    def can(self, permissions):
        return self.role is not None and \
            (self.role.permissions & permissions) == permissions


class AnonymousUser(AnonymousUserMixin):
    def can(self, _):
        return False


login.anonymous_user=AnonymousUser
@login.user_loader
def load_user(id):
    return db.session.get(User, int(id))
