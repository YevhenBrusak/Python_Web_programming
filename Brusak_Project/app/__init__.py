from flask import Flask
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, migrate
from flask_login import LoginManager
from config import config

bcrypt = Bcrypt()

login_manager = LoginManager()
login_manager.login_view = 'account.login'
login_manager.login_message_category = 'info'
db = SQLAlchemy()
migrate = Migrate()


def create_app(config_name = 'default'):
    app = Flask(__name__)
    app.config.from_object(config.get(config_name))

    db.init_app(app)
    migrate.init_app(app, db, render_as_batch=True)
    bcrypt.init_app(app)
    login_manager.init_app(app)

    with app.app_context():
        from app.home import home_bp
        from app.form_cabinet import cabinet_bp
        from app.account import account_bp
        from app.to_do import to_do_bp

        app.register_blueprint(home_bp)
        app.register_blueprint(cabinet_bp)
        app.register_blueprint(account_bp)
        app.register_blueprint(to_do_bp)

    return app