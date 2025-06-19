import os
from flask import Blueprint, request, jsonify
from src.database.models.user import User
from src.dependencies import login_manager
from src.database.db import db
from datetime import datetime, timedelta
from src.helper import token_required
import jwt

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")
userModel = db.select(User)


@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)


@auth_bp.route("/protected", methods=["GET"])
@token_required
def protected_route(user_id):
    return jsonify({"message": "Access granted", "user_id": user_id})


@auth_bp.route("/login", methods=["POST"])
def login():
    """
    Documentação
    """
    login_data = request.get_json()
    if not all(field in login_data for field in ("user", "password")):
        return (jsonify({"message": "Missing required fields"}), 400)

    stmt = userModel.filter_by(email=login_data["user"])
    user = db.session.execute(stmt).scalar_one_or_none()
    if not user:
        return (jsonify({"message": "Invalid email or password"}), 403)

    if not user.verify_password(login_data["password"]):
        return (jsonify({"message": "Invalid email or password"}), 403)

    token = jwt.encode(
        {
            "username": user.email,
            "user_id": user.id,
            "exp": datetime.now() + timedelta(hours=24),
        },
        os.getenv("SECRET_KEY"),
    )

    response = jsonify({"message": "Login successful", "token": token})
    response.set_cookie("token", token, httponly=True, secure=True, samesite="Strict")
    return (
        response,
        200,
    )
