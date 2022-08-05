import os
from venv import create

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path

from flask_caching import Cache
from flask_migrate import Migrate
from dotenv import load_dotenv


db = SQLAlchemy()  # SQL Alchemy instance
cache = Cache()
ENV_PATH = os.path.join(os.getcwd(), '.env')
load_dotenv(dotenv_path=ENV_PATH)
# DB_NAME = 'database.db'


def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('PRODUCTION_DB_URL')  # triple slash is a relative path
    
    db.init_app(app)
    cache = Cache(app, config={'CACHE_TYPE': 'simple'})

    from .flaskDB import User, Post
    # create_database(app)



    from .views import views
    from .cookies import cookies
    from .error import init_error

    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(cookies, url_prefix="/")
    init_error(app)

    # migrate = Migrate()
    # migrate.init_app(app, db, render_as_batch=True)




    return app

app = create_app()

def create_database(app):
    if not path.exists('website'+os.sep+DB_NAME):
        db.create_all(app=app)
        print('database created!')


def migrate_database():
    app = create_app()
    migrate = Migrate()
    migrate.init_app(app, db)
    return app
    
    