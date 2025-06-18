from flask import Blueprint, request, jsonify

users_bp = Blueprint("users", __name__, url_prefix="/users")