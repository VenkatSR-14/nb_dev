from sqlalchemy import Column, Integer, String, Boolean, Float, Text
from app.core.database import Base

from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, Boolean, Float, ForeignKey
from app.core.database import Base

class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    veg_non = Column(Boolean, nullable=False)
    height = Column(Float, nullable=False)
    weight = Column(Float, nullable=False)
    disease = Column(String, nullable=True)
    diet = Column(String, nullable=True)
    gender = Column(Boolean, nullable=False)

    # ✅ Fix: Add the "mapping" relationship
    mapping = relationship("UserMapping", back_populates="user", uselist=False)

