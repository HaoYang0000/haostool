from app.services.user.user_service import UserService
from functools import wraps
from flask import abort
from flask_login import current_user

def admin_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if current_user:
            print(current_user.id)
            if UserService().is_admin(user_id=current_user.id):
                return func(*args, **kwargs)
        else:
            abort(401)
        abort(403)
    return wrapper