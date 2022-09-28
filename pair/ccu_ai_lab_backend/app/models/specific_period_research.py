from .. import db
from .role import Role
from flask import current_app, request, url_for
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from werkzeug.security import generate_password_hash, check_password_hash
import hashlib
from datetime import datetime

class SpecificPeriodResearch(db.Model):
    __tablename__ = "specific_period_researches"
    id = db.Column(db.Integer, primary_key=True)
    research_id = db.Column(db.Integer, db.ForeignKey("researches.id"))
    specific_period_id = db.Column(db.Integer, db.ForeignKey("specific_periods.id"))
    updated_at = db.Column(db.DateTime(), default=datetime.utcnow)
    created_at = db.Column(db.DateTime(), default=datetime.utcnow)

    def to_json(self):
        result = {
            "id": self.id,
            "research_id": self.research_id,
            "specific_period_id": self.specific_period_id,
            "updated_at": self.updated_at.strftime("%Y-%m-%d %H:%M:%S"),
            "created_at": self.created_at.strftime("%Y-%m-%d %H:%M:%S")
        }
        return result

