from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from src.database.db import db
from src.extensions import bcrypt

class User(db.Model):
    __tablename__ = "users"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    birth: Mapped[str] = mapped_column(String(10), nullable=True)
    password: Mapped[str] = mapped_column(String(120), nullable=False)
    
    def __init__(self, name, email, birth, password):
        self.name = name
        self.email = email
        self.birth = birth
        self.password = password

    def verify_password(self, password: str) -> bool:
        is_password_valid = bcrypt.check_password_hash(self.password, password)
        return is_password_valid