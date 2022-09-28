from flask import Flask
from flask_mail import Mail
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from config import config
from flask_jwt_extended import JWTManager


jwt = JWTManager()

app = Flask(__name__)
CORS(app, supports_credentials=True)

mail = Mail()
moment = Moment()
db = SQLAlchemy()
migrate = Migrate(app, db)
blacklist = set()

def create_app(config_name):
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    jwt.init_app(app)
    mail.init_app(app)
    moment.init_app(app)

    from .models.research import Research
    from .models.user_research import UserResearch
    from .models.specific_period_research import SpecificPeriodResearch

    db.init_app(app)
    migrate.init_app(app, db)
    if app.config['SSL_REDIRECT']:
        from flask_sslify import SSLify
        sslify = SSLify(app)

    from .api import api as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/api/v1')

    return app
