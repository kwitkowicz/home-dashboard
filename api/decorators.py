from functools import wraps
from flask import abort
from flask_login import current_user
from api.models.user import Permission


def permission_required(permission):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.can(permission):
                abort(403)
            return f(*args, **kwargs)
        return decorated_function
    return decorator


def admin_required(f):
    return permission_required(Permission.ADMIN)(f)


def user_required(f):
    return permission_required(Permission.USER)(f)


def access_forbidden(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        abort(403)

    return wrapper
