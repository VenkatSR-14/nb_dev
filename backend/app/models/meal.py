from sqlalchemy import Column, Integer, String, Boolean, Float, Text, DECIMAL
from sqlalchemy.orm import relationship
from app.core.database import Base

class Meal(Base):
    """
    SQLAlchemy model for the `meals` table.
    """
    __tablename__ = "meals"

    meal_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    category = Column(String(50))
    description = Column(Text)
    veg_non = Column(Boolean, nullable=False)
    nutrient = Column(String(100))
    disease = Column(Text)
    diet = Column(Text)
    price = Column(DECIMAL(10, 2))

    # ✅ Relationship with user activity
    recent_activities = relationship("RecentActivity", back_populates="meal")
