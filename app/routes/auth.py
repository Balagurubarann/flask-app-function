from app.models.user import User
from app.config.db import db
from flask import request, jsonify, make_response
from flask_jwt_extended import create_access_token
from passlib.hash import bcrypt
from flask import Blueprint

auth = Blueprint('auth', __name__)

@auth.route('/register', methods=['POST'])
def register():

    data = request.get_json()

    username = data["username"]
    email = data["email"]
    password = data["password"]

    if not username or not email or not password:

        return jsonify({ "message": "Missing Fields", "success": False }), 400

    existing_user = User.query.filter((User.username == username) | (User.email == email)).first()

    if existing_user:

        return jsonify({ "message": "User already exists!", "success": False }), 409

    hashed_password = bcrypt.hash(password)

    new_user = User(
        username=username,
        email=email,
        password=hashed_password
    )

    db.session.add(new_user)
    db.session.commit()

    return jsonify({ "message": "User created successfully!", "success": True, "username": { new_user.username } }), 201

@auth.route('/login', methods=['POST'])
def login():

    data = request.get_json()

    print("Received Data: ", data)

    email = data.get("email")
    password = data.get("password")

    if not email or not password:

        return jsonify({ "message": "All fields are required!", "success": False }), 400

    email = data["email"]
    password = data["password"]

    user = User.query.filter_by(email=email).first()

    if not user:

        return jsonify({ "message": "Incorrect email or password", "success": False }), 401

    auth_user = bcrypt.verify(password, user.password)

    if not auth_user:

        return jsonify({ "message": "Incorrect email or password", "success": False }), 401

    access_token = create_access_token(identity=user.id)

    formatted_user = {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "created_on": user.created_on,
        "updated_on": user.updated_on
    }

    response = make_response(jsonify({ "message": "User logged in successfully", "success": True, "user": formatted_user }))

    response.set_cookie("access_token", access_token, httponly=True, samesite="Lax")

    return response, 200

@auth.route('/logout', methods=['POST'])
def logout():
    response = make_response({ "message": "user logged out successfully!", "success": True })
    response.set_cookie("access_token", "")

    return response, 200
