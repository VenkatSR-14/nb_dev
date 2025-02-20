from sqlalchemy import Column, Integer, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.core.database import Base
from datetime import datetime
from app.models.exercise import Exercise  # ✅ Import Exercise model


class RecentActivity(Base):
    """
    SQLAlchemy model for `user_activity` table.
    Tracks user interactions with meals and exercises.
    """
    __tablename__ = "user_activity"

    activity_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False)
    meal_id = Column(Integer, ForeignKey("meals.meal_id", ondelete="CASCADE"), nullable=True)
    exercise_id = Column(Integer, ForeignKey("exercises.exercise_id", ondelete="CASCADE"), nullable=True)
    rated = Column(Boolean, default=False)
    liked = Column(Boolean, default=False)
    searched = Column(Boolean, default=False)
    purchased = Column(Boolean, default=False)
    performed = Column(Boolean, default=False)
    duration = Column(Integer, nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow)

    # ✅ Relationships
    user = relationship("User", back_populates="recent_activities")
    meal = relationship("Meal", back_populates="recent_activities")
    exercise = relationship("Exercise", back_populates="recent_activities")  # ✅ Added relationship
