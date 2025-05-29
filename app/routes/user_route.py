from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import Blueprint, request, jsonify
from app.models.user import User
from app.middleware.verifyUser import verify_user
from openpyxl import Workbook

user = Blueprint("user", __name__)

@user.route("/get-users", methods=["GET"])
@verify_user
def get_users():

    users = User.query.order_by(User.username.asc()).all()

    if not users:

        return jsonify({ "message": "No users found" }), 200

    users_list = [{ "id": user.id, "username": user.username, "email": user.email, "created_on": user.created_on, "updated_on": user.updated_on } for user in users]

    return jsonify({ "message": "Users data fetched successfully!", "success": True, "users": users_list }), 200

@user.route("/extract-csv", methods=["POST"])
def extract_csv():

    text_data = request.form["text_data"]

    if not text_data:

        return jsonify({ "message": "no text found", "success": False }), 404

    lines = text_data.splitlines()

    wb = Workbook()
    ws = wb.active

    for i, line in enumerate(lines, start=1):

        ws.cell(row=i, column=1, value=line)

    wb.save("output.xlsx")

    return jsonify({ "message": "Excel file created!", "success": True }), 200
