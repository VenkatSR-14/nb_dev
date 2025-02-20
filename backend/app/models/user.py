from sqlalchemy import Column, Integer, String, Boolean, Float, Text
from sqlalchemy.orm import relationship
from app.core.database import Base
from app.models.recommendations import Recommendation
class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    veg_non = Column(Boolean, nullable=False)
    height = Column(Float, nullable=False)
    weight = Column(Float, nullable=False)
    disease = Column(Text, nullable=True)  # Changed to Text to match schema
    diet = Column(Text, nullable=True)     # Changed to Text to match schema
    gender = Column(Boolean, nullable=False)

    # ✅ Relationship with UserMapping
    mapping = relationship("UserMapping", back_populates="user", uselist=False)

    # ✅ Relationship with RecentActivity (UserActivity table)
    recent_activities = relationship("RecentActivity", back_populates="user", cascade="all, delete-orphan")

    # ✅ Relationship with Recommendations (New Fix)
    recommendations = relationship("Recommendation", back_populates="user", cascade="all, delete-orphan")
