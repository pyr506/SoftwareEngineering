from .. import db
from flask import current_app, request, url_for
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
import hashlib
from datetime import datetime

class COPI_project(db.Model):

    __tablename__ = 'COPI_project'
    id = db.Column(db.Integer, primary_key=True)
    specific_period_id = db.Column(db.Integer, db.ForeignKey('specific_periods.id', ondelete='CASCADE'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    COPI_content = db.Column(db.Text, default="")
    accepted = db.Column(db.Boolean, default=False)
    updated_at = db.Column(db.DateTime(), default=datetime.utcnow)
    created_at = db.Column(db.DateTime(), default=datetime.utcnow)

    def to_json(self):
        result = {
            'id': self.id if self.id != None else "",
            'specific_period_id': self.specific_period_id if self.specific_period_id != None else "",
            'user_id': self.user_id if self.user_id != None else "",
            'user_name': self.user.username if self.user.username != None else "",
            'accepted': self.accepted if self.accepted != None else "",
            'COPI_content': self.COPI_content if self.COPI_content != None else "",
            'updated_at': self.updated_at.strftime("%Y-%m-%d %H:%M:%S"),
            'created_at': self.created_at.strftime("%Y-%m-%d %H:%M:%S")
        }
        return result