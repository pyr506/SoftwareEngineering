from .. import db
from flask import current_app, request, url_for
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
import hashlib
from datetime import datetime

class Webinfo(db.Model):

    __tablename__ = 'webinfos'
    id = db.Column(db.Integer, primary_key=True)
    tel = db.Column(db.String(128), default="")
    email = db.Column(db.String(128), default="")
    address = db.Column(db.String(256), default="")
    link = db.Column(db.String(256), default="")

    def to_json(self):
        result = {
            'id': self.id if self.id != None else "",
            'tel': self.tel if self.tel != None else "",
            'email': self.email if self.email != None else "",
            'address': self.address if self.address != None else "",
            'link': self.link if self.link != None else ""
        }
        return result