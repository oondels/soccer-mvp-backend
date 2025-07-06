from datetime import datetime
from sqlalchemy import Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from src.database.db import db


class Team(db.Model):
    __tablename__ = "teams"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(String(350), nullable=True)
    team_profile_image: Mapped[str] = mapped_column(String(255), nullable=True)
    team_banner_image: Mapped[str] = mapped_column(String(255), nullable=True)
    captain_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id"), nullable=True
    )
    is_active: Mapped[bool] = mapped_column(Integer, default=1, nullable=False)
    ranking_points: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    members_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    notes: Mapped[str] = mapped_column(String(350), nullable=True)
    create_date: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, nullable=False
    )
    update_date: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )

    def __init__(self, name=None):
        self.name = name
