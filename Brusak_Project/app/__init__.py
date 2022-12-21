from flask import Flask
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, migrate
from flask_login import LoginManager
from flask_jwt_extended import JWTManager
from config import config

bcrypt = Bcrypt()

login_manager = LoginManager()
login_manager.login_view = 'account.login'
login_manager.login_message_category = 'info'
db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()


def create_app(config_name = 'default'):
    app = Flask(__name__)
    app.config.from_object(config.get(config_name))

    db.init_app(app)
    migrate.init_app(app, db, render_as_batch=True)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    jwt.init_app(app)

    with app.app_context():
        from app.home import home_bp
        from app.form_cabinet import cabinet_bp
        from app.account import account_bp
        from app.to_do import to_do_bp
        from app.category_api import category_api_bp
        from app.task_api import task_api_bp
        from app.swagger import swagger_bp

        app.register_blueprint(home_bp)
        app.register_blueprint(cabinet_bp)
        app.register_blueprint(account_bp)
        app.register_blueprint(to_do_bp)
        app.register_blueprint(category_api_bp, url_prefix='/api')
        app.register_blueprint(task_api_bp, url_prefix='/api/v2')
        app.register_blueprint(swagger_bp)

    return app