from flask import Blueprint, request, jsonify
from src.database.models.user import User
from src.database.db import db
from src.dependencies import bcrypt

users_bp = Blueprint("users", __name__, url_prefix="/users")
userModel = db.select(User)


@users_bp.route("/", methods=["GET"])
def get_users():
    users = db.session.execute(userModel.order_by(User.id)).scalars().all()

    user_list = [
        {
            "id": user.id,
            "name": user.name,
        }
        for user in users
    ]
    return jsonify({"users": user_list}), 200


@users_bp.route("/", methods=["POST"])
def create_user():
    user_data = request.get_json()

    stmt = userModel.filter_by(email=user_data["email"])
    existing_user = db.session.execute(stmt).scalar_one_or_none()
    if existing_user:
        return jsonify({"message": "Email already in use"}), 400

    if not all(field in user_data for field in ("name", "email", "password")):
        return jsonify({"message": "Missing required fields"}), 400

    hashed_password = bcrypt.generate_password_hash(user_data["password"]).decode(
        "utf-8"
    )
    new_user = User(
        name=user_data["name"],
        email=user_data["email"],
        birth=user_data["birth"],
        password=hashed_password,
    )

    db.session.add(new_user)
    db.session.commit()

    return (
        jsonify(
            {
                "message": "User created successfully",
                "user": {
                    "id": new_user.id,
                    "name": new_user.name,
                },
            }
        ),
        201,
    )


@users_bp.route("/<int:id>", methods=["PUT"])
def edit_user(id):
    stmt = userModel.filter_by(id=id)
    user = db.session.execute(stmt).scalar_one_or_none()
    if not user:
        return (jsonify({"message": "User not found"}), 404)

    return f"Editing user with id {id}"
