from flask import Flask, session
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
import urllib.parse

db = SQLAlchemy()
# jwt = JWTManager()


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'secret key'
    username = 'root'
    password = urllib.parse.quote_plus('Unik@1234')
    hostname = 'localhost'
    database = 'Banking_system'
    app.config["SQLALCHEMY_DATABASE_URI"] = f"mysql+pymysql://{username}:{password}@{hostname}:3306/{database}"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    # jwt.init_app(app)
    

    from app.controllers.signup import signup_bp
    app.register_blueprint(signup_bp)
    from app.controllers.login import login_bp
    app.register_blueprint(login_bp)
    from app.controllers.transactions import transaction_bp
    app.register_blueprint(transaction_bp)
    from app.controllers.logout import logout_bp
    app.register_blueprint(logout_bp)
    from app.controllers.banker import user_accounts_bp
    app.register_blueprint(user_accounts_bp)

    return app


print("Hello World")
