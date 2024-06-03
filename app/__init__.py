from flask import Flask, session
from flask_sqlalchemy import SQLAlchemy
import urllib.parse
from datetime import timedelta 

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'secret key'
    username = 'root'
    password = urllib.parse.quote_plus('Unik@1234')
    hostname = 'localhost'
    database = 'Banking_system'
    app.config["SQLALCHEMY_DATABASE_URI"] = f"mysql+pymysql://{username}:{password}@{hostname}:3306/{database}"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    # app.config['PERMANENT_SESSION_LIFETIME'] =  timedelta(seconds=10)
    db.init_app(app)

    

    from app.auth import auth_bp
    app.register_blueprint(auth_bp,url_prefix='/auth')

    from app.md import transaction_bp
    app.register_blueprint(transaction_bp,url_prefix='/transaction')

    from app.auth import index_bp
    app.register_blueprint(index_bp)

    return app

