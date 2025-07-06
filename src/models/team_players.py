from datetime import datetime
from sqlalchemy import Integer, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.database.db import db


class TeamPlayer(db.Model):
    __tablename__ = "team_players"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id"), nullable=False
    )
    team_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("teams.id"), nullable=False
    )
    create_date: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, nullable=False
    )
    update_date: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )
    
    user = relationship("User", backref="team_memberships")
    team = relationship("Team", backref="team_players")
    
    __table_args__ = (
        UniqueConstraint('user_id', 'team_id', name='unique_user_team'),
    )
    
    def __init__(self, user_id=None, team_id=None):
        self.user_id = user_id
        self.team_id = team_id
