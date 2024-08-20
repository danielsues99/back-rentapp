from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from .config import Config

db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
bcrypt = Bcrypt()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)
    bcrypt.init_app(app)

    login.login_view = 'api.login'
    login.session_protection = "strong"

    with app.app_context():
        from app import routes, models

    from app import routes, models
    app.register_blueprint(routes.bp)

    return app

@login.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
