from .. import db
from markdown import markdown
import bleach
from flask import current_app, request, url_for
from datetime import datetime

class News(db.Model):
    __tablename__ = 'news'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(256),default="")
    content = db.Column(db.Text)
    clicked = db.Column(db.Integer, default=0)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    location = db.Column(db.String(64))
    updated_at = db.Column(db.DateTime(), default=datetime.utcnow)
    created_at = db.Column(db.DateTime(), default=datetime.utcnow)

    def to_json(self):
        result = {
            'id': self.id if self.id != None else "",
            'title': self.title if self.title != None else "",
            'content': self.content if self.content != None else "",
            'clicked': self.clicked if self.clicked != None else 0,
            'location': self.location if self.location != None else "",
            'updated_at': self.updated_at.strftime("%Y-%m-%d %H:%M:%S"),
            'created_at': self.created_at.strftime("%Y-%m-%d %H:%M:%S")
        }
        return result
