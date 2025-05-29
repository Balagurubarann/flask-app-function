from flask import Flask
from flask_cors import CORS
from app.config import db
from app.routes.auth import auth
from app.routes.user_route import user

def create_app():

    app = Flask(__name__)

    CORS(app, supports_credentials=True, origins=["http://localhost:5173"])

    app.register_blueprint(auth, url_prefix="/auth")
    app.register_blueprint(user, url_prefix="/user")

    db.init_db(app)

    return app
