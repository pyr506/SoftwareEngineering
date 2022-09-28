from functools import wraps
from flask_login import current_user
from app.models.permission import Permission
from flask import jsonify, request, current_app, url_for, Blueprint
from . import api, response
from .. import blacklist
from ..models.user import User
from ..models.setting import Setting
import json
from datetime import datetime, date

from flask_jwt_extended import (
    decode_token
)
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

def token_required(f):
   @wraps(f)
   def decorator(*args, **kwargs):
        token = None

        if 'x-access-tokens' in request.headers:
            token = request.headers['x-access-tokens']

        if not token:
            return response.error(403, "Access Denied, Please Login First.")

        try:
            data = decode_token(token)
            if data['jti'] in blacklist:
                return response.error(403, "Token is invalid")
            current_user = User.query.filter_by(email=data['sub']).first()
        except Exception as e:
            print(str(e))
            return response.error(403, "Token is invalid")

        return f(current_user, *args, **kwargs)
   return decorator

def in_speific_period_time(f):
   @wraps(f)
   def decorator(*args, **kwargs):
        setting = Setting.query.filter_by(key='period_of_time').first()
        period_of_time_obj = json.loads(setting.value)
        start = date(year=int(period_of_time_obj["start"].split('-')[0]),month=int(period_of_time_obj["start"].split('-')[1]),day=int(period_of_time_obj["start"].split('-')[2]))
        end = date(year=int(period_of_time_obj["end"].split('-')[0]),month=int(period_of_time_obj["end"].split('-')[1]),day=int(period_of_time_obj["end"].split('-')[2]))
        today = date.today()

        if start > today or today > end:
            return response.error(403, 'Not in the specific period time.')

        return f(start, end, *args, **kwargs)
   return decorator
