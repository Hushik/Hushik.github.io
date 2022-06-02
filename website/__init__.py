from fileinput import filename
from flask import Flask, url_for, request
from flask_sqlalchemy import SQLAlchemy
from os import path
from werkzeug.utils import secure_filename
import os
from flask_login import LoginManager




db = SQLAlchemy()
DB_NAME = "database.db"

qwerty = ""



def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'ey7tbtb7t78'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

    from .models import User

    login_manager = LoginManager(app)
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import Locomotive
    print(app.instance_path)
    qwerty = app.instance_path
    create_database(app)

    return app

def create_database(app):
    if not path.exists("website/" + DB_NAME):
        db.create_all(app=app)
        print("Created database!")


