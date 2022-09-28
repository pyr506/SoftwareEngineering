from .. import db
from .role import Role
from flask import current_app, request, url_for
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from werkzeug.security import generate_password_hash, check_password_hash
import hashlib
from datetime import datetime

class SpecificPeriod(db.Model):
    __tablename__ = "specific_periods"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    country = db.Column(db.String(64), default="")
    university = db.Column(db.String(64), default="")
    name_of_pi = db.Column(db.String(64), default="")
    department = db.Column(db.String(64), default="")
    start_date = db.Column(db.DateTime(), default=datetime.utcnow)
    end_date = db.Column(db.DateTime(), default=datetime.utcnow)
    apply_copi_end_date = db.Column(db.DateTime(), default=datetime.utcnow)
    project_title = db.Column(db.String(256), default="")
    project_content = db.Column(db.Text, default="")
    link = db.Column(db.String(256), default="")
    location = db.Column(db.String(64), default="0.0.0.0")
    updated_at = db.Column(db.DateTime(), default=datetime.utcnow)
    created_at = db.Column(db.DateTime(), default=datetime.utcnow)
    specific_period_researches = db.relationship("SpecificPeriodResearch", backref="specific_period", lazy="dynamic", cascade="all, delete-orphan")

    def to_json(self):
        specific_period_researches = self.specific_period_researches
        specific_period_researches_array = []
        for specific_period_research in specific_period_researches:
            specific_period_researches_array.append(specific_period_research.research.to_json())

        result = {
            "id": self.id,
            "user_name": self.user.username,
            "user_id": self.user_id,
            "country": self.country,
            "university": self.university,
            "department": self.department,
            "name_of_pi": self.name_of_pi,
            "researches": specific_period_researches_array,
            "start_date": self.start_date.strftime("%Y-%m-%d %H:%M:%S"),
            "end_date": self.end_date.strftime("%Y-%m-%d %H:%M:%S"),
            "apply_copi_end_date": self.apply_copi_end_date.strftime("%Y-%m-%d %H:%M:%S"),
            "project_title": self.project_title,
            "project_content": self.project_content,
            "link": self.link,
            "updated_at": self.updated_at.strftime("%Y-%m-%d %H:%M:%S"),
            "created_at": self.created_at.strftime("%Y-%m-%d %H:%M:%S")
        }
        return result

