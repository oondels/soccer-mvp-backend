from flask import Blueprint, request, jsonify
from src.models.user import User
from src.database.db import db
from src.extensions import bcrypt

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


@users_bp.route("/<int:id>", methods=["GET"])
def get_user(id):
    """
    Get a user by ID
    ---
    tags:
      - Users
    parameters:
      - in: path
        name: id
        required: true
        schema:
          type: integer
        description: The ID of the user to retrieve
    responses:
      200:
        description: User found
        content:
          application/json:
            schema:
              type: object
              properties:
                id:
                  type: integer
                name:
                  type: string
                email:
                  type: string
                birth:
                  type: string
      404:
        description: User not found
    """
    stmt = userModel.filter_by(id=id)
    user = db.session.execute(stmt).scalar_one_or_none()
    if not user:
        return jsonify({"message": "User not found"}), 404

    return (
        jsonify(
            {
                "id": user.id,
                "name": user.name,
                "email": user.email,
                "birth": user.birth,
            }
        ),
        200,
    )


@users_bp.route("/", methods=["POST"])
def create_user():
    """
    Create a new user
    ---
    tags:
      - Users
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            properties:
              name:
                type: string
              email:
                type: string
              password:
                type: string
              birth:
                type: string
    responses:
      201:
        description: User created successfully
      400:
        description: Email already exists
    """
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
    """Update an existing user
    ---
    tags:
      - Users
    parameters:
      - in: path
        name: id
        required: true
        schema:
          type: integer
        description: The ID of the user to update
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            properties:
              name:
                type: string
              email:
                type: string
              birth:
                type: string
              password:
                type: string
    responses:
      200:
        description: User updated successfully
      400:
        description: Email already in use
      404:
        description: User not found
    """
    stmt = userModel.filter_by(id=id)
    user = db.session.execute(stmt).scalar_one_or_none()
    if not user:
        return jsonify({"message": "User not found"}), 404

    user_data = request.get_json()

    if "email" in user_data and user_data["email"] != user.email:
        email_stmt = userModel.filter_by(email=user_data["email"])
        existing_user = db.session.execute(email_stmt).scalar_one_or_none()
        if existing_user:
            return jsonify({"message": "Email already in use"}), 400
        user.email = user_data["email"]

    if "name" in user_data:
        user.name = user_data["name"]

    if "birth" in user_data:
        user.birth = user_data["birth"]

    db.session.commit()

    return (
        jsonify(
            {
                "message": "User updated successfully",
                "user": {
                    "id": user.id,
                    "name": user.name,
                    "email": user.email,
                    "birth": user.birth,
                },
            }
        ),
        200,
    )
