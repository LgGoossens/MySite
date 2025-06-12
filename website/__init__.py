import os.path

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

from dotenv import load_dotenv

db = SQLAlchemy()
DB_NAME = 'database.db'


def create_app():
    print(os.getcwd())
    app = Flask(__name__)
    load_dotenv('/resources/.env')
    app.config['SECRET_KEY'] = "bRRJPqnYC1cbmGmJ9DQ8kJUgTOg6Ig"
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/auth')

    from . import models

    create_database(app)

    loginManager = LoginManager()
    loginManager.login_view = 'auth.login'
    loginManager.init_app(app)

    @loginManager.user_loader
    def loadUser(id):
        return models.User.query.get(int(id))

    return app


def create_database(app):
    if not os.path.exists('instance/' + DB_NAME):
        with app.app_context():
            db.create_all()
        print('database created!')
