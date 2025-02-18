from sqlalchemy import Column, Integer, String, Boolean, Float, Text
from core.database import Base

class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    password_hash = Column(Text, nullable=False)
    email = Column(String, unique=True, nullable=False)
    veg_non = Column(Boolean)
    height = Column(Float, nullable=True)
    weight = Column(Float, nullable=True)
    bmi = Column(Float, nullable=True)  # Auto-calculated in DB
    nutrient = Column(String(100), nullable=True)
    disease = Column(Text, nullable=True)
    diet = Column(Text, nullable=True)
