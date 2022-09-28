from .. import db
from .role import Role
from flask import current_app, request, url_for
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from werkzeug.security import generate_password_hash, check_password_hash
import hashlib
from datetime import datetime

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    first_name = db.Column(db.String(64), default="")
    last_name = db.Column(db.String(64), default="")
    username = db.Column(db.String(64), default="")
    country = db.Column(db.String(100), default="")
    company = db.Column(db.String(128), default="")
    job_title = db.Column(db.String(50), default="")
    about_me = db.Column(db.Text(), default="")
    role_id = db.Column(db.Integer, db.ForeignKey("roles.id"))
    password_hash = db.Column(db.String(128))
    confirmed_hash = db.Column(db.String(128))
    confirmed = db.Column(db.Boolean, default=True)
    blocked = db.Column(db.Boolean, default=False)
    location = db.Column(db.String(64), default="0.0.0.0")
    last_seen = db.Column(db.DateTime(), default=datetime.utcnow)
    avatar_hash = db.Column(db.String(32), default="")
    user_researches = db.relationship("UserResearch", backref="user", cascade="all, delete-orphan")
    news = db.relationship("News", backref="user", lazy="dynamic", cascade="all, delete-orphan")
    specific_periods = db.relationship("SpecificPeriod", backref="user", lazy="dynamic", cascade="all, delete-orphan")
    COPI_project = db.relationship("COPI_project", backref="user", lazy="dynamic", cascade="all, delete-orphan")

    updated_at = db.Column(db.DateTime(), default=datetime.utcnow)
    created_at = db.Column(db.DateTime(), default=datetime.utcnow)

    @staticmethod
    def initial():
        password = generate_password_hash(current_app.config["APP_ADMIN_PASSWORD"])
        user = User(email="servermis@ccu.com",username="servermis", company="CCU", job_title="MIS", password_hash=password,confirm=1)
        db.session.add(user)
        db.session.commit()

    @staticmethod
    def add_self_follows():
        for user in User.query.all():
            if not user.is_following(user):
                user.follow(user)
                db.session.add(user)
                db.session.commit()

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)

    @property
    def password(self):
        raise AttributeError("password is not a readable attribute")

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    @property
    def confirmed_email(self):
        raise AttributeError("confirmed_email is not a readable attribute")
    
    @confirmed_email.setter
    def confirmed_email(self, confirmed_email):
        self.confirmed_hash = generate_password_hash(confirmed_email)
    
    def verify_confirmed_email(self, confirmed_email):
        if self.confirmed_hash=="pbkdf2:sha256:50000$" + confirmed_email:
            return True
        else:
            return False

    def generate_confirmation_token(self, expiration=3600):
        s = Serializer(current_app.config["SECRET_KEY"], expiration)
        return s.dumps({"confirm": self.id}).decode("utf-8")

    def confirm(self, token):
        s = Serializer(current_app.config["SECRET_KEY"])
        try:
            data = s.loads(token.encode("utf-8"))
        except:
            return False
        if data.get("confirm") != self.id:
            return False
        self.confirmed = True
        db.session.add(self)
        return True

    def generate_reset_token(self, expiration=3600):
        s = Serializer(current_app.config["SECRET_KEY"], expiration)
        return s.dumps({"reset": self.id}).decode("utf-8")

    @staticmethod
    def reset_password(token, new_password):
        s = Serializer(current_app.config["SECRET_KEY"])
        try:
            data = s.loads(token.encode("utf-8"))
        except:
            return False
        user = User.query.get(data.get("reset"))
        if user is None:
            return False
        user.password = new_password
        db.session.add(user)
        return True

    def generate_email_change_token(self, new_email, expiration=3600):
        s = Serializer(current_app.config["SECRET_KEY"], expiration)
        return s.dumps(
            {"change_email": self.id, "new_email": new_email}).decode("utf-8")

    def change_email(self, token):
        s = Serializer(current_app.config["SECRET_KEY"])
        try:
            data = s.loads(token.encode("utf-8"))
        except:
            return False
        if data.get("change_email") != self.id:
            return False
        new_email = data.get("new_email")
        if new_email is None:
            return False
        if self.query.filter_by(email=new_email).first() is not None:
            return False
        self.email = new_email
        self.avatar_hash = self.gravatar_hash()
        db.session.add(self)
        return True

    def can(self, perm):
        return self.role is not None and self.role.has_permission(perm)

    def is_administrator(self):
        return self.can(Permission.ADMIN)

    def ping(self):
        self.last_seen = datetime.utcnow()
        db.session.add(self)

    def gravatar_hash(self):
        return hashlib.md5(self.email.lower().encode("utf-8")).hexdigest()

    def gravatar(self, size=100, default="identicon", rating="g"):
        url = "https://secure.gravatar.com/avatar"
        hash = self.avatar_hash or self.gravatar_hash()
        return "{url}/{hash}?s={size}&d={default}&r={rating}".format(
            url=url, hash=hash, size=size, default=default, rating=rating)

    def follow(self, user):
        if not self.is_following(user):
            f = Follow(follower=self, followed=user)
            db.session.add(f)

    def unfollow(self, user):
        f = self.followed.filter_by(followed_id=user.id).first()
        if f:
            db.session.delete(f)

    def is_following(self, user):
        if user.id is None:
            return False
        return self.followed.filter_by(
            followed_id=user.id).first() is not None

    def is_followed_by(self, user):
        if user.id is None:
            return False
        return self.followers.filter_by(
            follower_id=user.id).first() is not None

    @property
    def followed_posts(self):
        return News.query.join(Follow, Follow.followed_id == News.author_id)\
            .filter(Follow.follower_id == self.id)

    def to_json(self):
        user_researches = self.user_researches
        user_researches_array = []
        for user_research in user_researches:
            user_researches_array.append(user_research.research.to_json())
            
        result = {
            "id": self.id if self.id != None else "",
            "email": self.email if self.email != None else "",
            "role": self.role.name if self.role != None else "",
            "first_name": self.first_name if self.first_name != None else "",
            "last_name": self.last_name if self.last_name != None else "",
            "username": self.username if self.username != None else "",
            "role_id": self.role_id if self.role_id != None else "",
            "country": self.country if self.country != None else "",
            "company": self.company if self.company != None else "",
            "job_title": self.job_title if self.job_title != None else "",
            "about_me": self.about_me if self.about_me != None else "",
            "researches": user_researches_array,
            "confirmed": self.confirmed if self.confirmed != None else "",
            "blocked": self.blocked if self.blocked != None else "",
            "location": self.location if self.location != None else "",
            "last_seen": self.last_seen.strftime("%Y-%m-%d %H:%M:%S"),
            "updated_at": self.updated_at.strftime("%Y-%m-%d %H:%M:%S"),
            "created_at": self.created_at.strftime("%Y-%m-%d %H:%M:%S")
        }
        return result

    def generate_auth_token(self, expiration):
        s = Serializer(current_app.config["SECRET_KEY"],
                       expires_in=expiration)
        return s.dumps({"id": self.id}).decode("utf-8")

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(current_app.config["SECRET_KEY"])
        try:
            data = s.loads(token)
        except:
            return None
        return User.query.get(data["id"])

    def __repr__(self):
        return "<User %r>" % self.username

def load_user(user_id):
    return User.query.get(int(user_id))
