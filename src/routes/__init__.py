from .users_route import users_bp
from .auth_route import auth_bp

def register_routes(app):
    app.register_blueprint(users_bp)
    app.register_blueprint(auth_bp)