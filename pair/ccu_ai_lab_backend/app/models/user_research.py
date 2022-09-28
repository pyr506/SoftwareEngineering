from flask_login import  AnonymousUserMixin
from .. import db
from flask import current_app, request, url_for
from datetime import datetime

class UserResearch(db.Model):
    __tablename__ = 'user_researches'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    # 0 or 1 means self research or wanna
    research_id = db.Column(db.Integer, db.ForeignKey('researches.id'))
    updated_at = db.Column(db.DateTime(), default=datetime.utcnow)
    created_at = db.Column(db.DateTime(), default=datetime.utcnow)