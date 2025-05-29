from flask_jwt_extended import decode_token
from flask import request, jsonify, g
from functools import wraps

def verify_user(fn):

    @wraps(fn)
    def decorated_function(*args, **kwargs):
        try:
            token = request.cookies.get('access_token')
            if not token:
                return jsonify({"message": "Token is missing", "success": False}), 401

            decoded_token = decode_token(token)
            user_id = decoded_token['sub']

            g.user_id = user_id

        except Exception as e:
            return jsonify({"message": "Token is invalid", "success": False}), 401

        return fn(*args, **kwargs)

    return decorated_function
