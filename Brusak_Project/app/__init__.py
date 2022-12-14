from flask import Flask
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, migrate
from flask_login import LoginManager
from flask_ckeditor import CKEditor
from flask_jwt_extended import JWTManager
from config import config
import sqlalchemy as sa
from click import echo

bcrypt = Bcrypt()

login_manager = LoginManager()
login_manager.login_view = 'account.login'
login_manager.login_message_category = 'info'
db = SQLAlchemy()
migrate = Migrate()
ckeditor = CKEditor()
jwt = JWTManager()


def create_app(config_name = 'default'):
    app = Flask(__name__)
    app.config.from_object(config.get(config_name))

    db.init_app(app)
    migrate.init_app(app, db, render_as_batch=True)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    ckeditor.init_app(app)
    jwt.init_app(app)
    register_cli_commands(app)

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

        engine = sa.create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
        inspector = sa.inspect(engine)
        if not inspector.has_table("users"):
            with app.app_context():
                db.drop_all()
                db.create_all()
                app.logger.info('Initialized the database!')
        else:
            app.logger.info('Database already contains the users table.')

    return app

def register_cli_commands(app):
    @app.cli.command('init_db')
    def initialize_database():
        """Initialize the database."""
        db.drop_all()
        db.create_all()
        echo('Initialized the database!')
