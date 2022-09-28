from .. import db
from markdown import markdown
import bleach
from flask import current_app, request, url_for
from datetime import datetime

class Chat(db.Model):
    __tablename__ = 'chat'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    cookie = db.Column(db.Text)
    user_content = db.Column(db.Text)
    ai_content = db.Column(db.Text)
    status = db.Column(db.Integer, default=0)
    updated_at = db.Column(db.DateTime(), default=datetime.utcnow)
    created_at = db.Column(db.DateTime(), default=datetime.utcnow)

    def to_json(self):
        result = {
            'id': self.id if self.id != None else "",
            'user_id': self.user_id if self.user_id != None else "",
            'cookie': self.cookie if self.cookie != None else "",
            'user_content': self.user_content if self.user_content != None else "",
            'ai_content': self.ai_content if self.ai_content != None else "",
            'status': self.status if self.status != None else "",
            'updated_at': self.updated_at.strftime("%Y-%m-%d %H:%M:%S"),
            'created_at': self.created_at.strftime("%Y-%m-%d %H:%M:%S")
        }
        return result
