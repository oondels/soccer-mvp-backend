from flask import request, jsonify, current_app
from functools import wraps
import jwt


def token_required(f):
    """
    Decorator to check if a valid JWT token is present in the request cookies.
    If the token is valid, it extracts the user ID and passes it to the decorated function.
    If the token is missing, expired, or invalid, it returns an error response."""
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.cookies.get("token")

        if not token:
            return (
                jsonify(
                    {"message": "Auth token is required", "error": "Token not found"}
                ),
                401,
            )

        try:
            data = jwt.decode(
                token, current_app.config["SECRET_KEY"], algorithms=["HS256"]
            )
            current_user_id = data["user_id"]

        except jwt.ExpiredSignatureError:
            return (
                jsonify({"message": "Token has expired", "error": "expired_token"}),
                401,
            )

        except jwt.InvalidTokenError:
            return (
                jsonify({"message": "Token is invalid", "error": "invalid_token"}),
                401,
            )

        return f(current_user_id, *args, **kwargs)

    return decorated
