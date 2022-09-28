from .. import db
from .role import Role
from flask import current_app, request, url_for
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from werkzeug.security import generate_password_hash, check_password_hash
import hashlib
from datetime import datetime
import json

class Setting(db.Model):
    __tablename__ = 'settings'
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(256), default="")
    value = db.Column(db.String(256), default="")
    updated_at = db.Column(db.DateTime(), default=datetime.utcnow)
    created_at = db.Column(db.DateTime(), default=datetime.utcnow)

    def to_json(self):
        result = {
            'id':self.id,
            'key':self.key,
            'value': self.value,
            'updated_at': self.updated_at.strftime("%Y-%m-%d %H:%M:%S"),
            'created_at': self.created_at.strftime("%Y-%m-%d %H:%M:%S")
        }
        return result

    @staticmethod
    def initial():
        value = {
            "start" : "2020-01-01",
            "end": "2099-12-31"
        }
        setting = Setting(key="period_of_time",value=json.dumps(value))
        db.session.add(setting)
        db.session.commit()
