from os import path
from flask import Flask
from .views import views
from .auth import auth
from flask_sqlalchemy import SQLAlchemy
 
db = SQLAlchemy()
DB_NAME = "database.db"

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'gsdgslkgksgklsk'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    
    from .models import User,Note

    create_datebase(app)
    return app


def create_datebase(app):
    if not path.exists('website/'+ DB_NAME):
        with app.app_context():
            db.create_all()
        print('Created Database!')
