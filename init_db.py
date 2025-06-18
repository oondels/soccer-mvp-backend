from src import create_app
from src.database.db import db
from src.database.models.user import User

app = create_app()

with app.app_context():
    print("Creating database tables...")
    db.create_all()
    print("Database tables created successfully!")