from .. import db
from flask import current_app, request, url_for
from datetime import datetime

class Research(db.Model):
    __tablename__ = 'researches'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, index=True)
    updated_at = db.Column(db.DateTime(), default=datetime.utcnow)
    created_at = db.Column(db.DateTime(), default=datetime.utcnow)
    user_research = db.relationship("UserResearch", backref="research")
    specific_period_research = db.relationship("SpecificPeriodResearch", backref="research")

    @staticmethod
    def initial():
        research1 = Research(name="Demo1")
        research2 = Research(name="Demo2")
        db.session.add(research1)
        db.session.add(research2)
        db.session.commit()

    def __init__(self, **kwargs):
        super(Research, self).__init__(**kwargs)

    def to_json(self):
        json_post = {
            'id': self.id,
            'name': self.name
        }
        return json_post
