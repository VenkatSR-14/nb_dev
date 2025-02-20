from sqlalchemy import Column, Integer, ForeignKey, Text, DateTime
from sqlalchemy.orm import relationship
from app.core.database import Base
from datetime import datetime

class Recommendation(Base):
    """
    Stores recommended meals & exercises for a user.
    """
    __tablename__ = "recommendations"

    recommendation_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False)
    meal_id = Column(Integer, ForeignKey("meals.meal_id", ondelete="CASCADE"), nullable=True)
    exercise_id = Column(Integer, ForeignKey("exercises.exercise_id", ondelete="CASCADE"), nullable=True)
    recommendation_reason = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

    # ✅ Relationships
    user = relationship("User", back_populates="recommendations")
