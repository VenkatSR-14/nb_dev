from sqlalchemy import Column, Integer, String, Boolean, Float
from app.core.database import Base

class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    veg_non = Column(Boolean)
    height = Column(Float)
    weight = Column(Float)
    bmi = Column(Float)  # Auto-generated in DB
    disease = Column(String)
