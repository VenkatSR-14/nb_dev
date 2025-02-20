from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import relationship
from app.core.database import Base

class Exercise(Base):
    """
    SQLAlchemy model for the `exercises` table.
    """
    __tablename__ = "exercises"

    exercise_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    calories_burned = Column(Float, nullable=False)
    target_weight = Column(Float, nullable=True)
    actual_weight = Column(Float, nullable=True)
    age = Column(Integer, nullable=True)
    gender = Column(String(10), nullable=True)
    duration = Column(Integer, nullable=False)
    heart_rate = Column(Integer, nullable=True)
    bmi = Column(Float, nullable=True)
    weather_conditions = Column(String(50), nullable=True)
    intensity = Column(Integer, nullable=True)

    # ✅ Relationship with `RecentActivity`
    recent_activities = relationship("RecentActivity", back_populates="exercise")
