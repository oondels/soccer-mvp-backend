from .users_route import users_bp

def register_routes(app):
    app.register_blueprint(users_bp)