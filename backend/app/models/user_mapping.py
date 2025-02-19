from sqlalchemy import ForeignKey, Column, Integer, String
from app.core.database import Base
from sqlalchemy.orm import relationship

class UserMapping(Base):
    __tablename__ = "user_mapping"

    user_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"), primary_key=True)
    username = Column(String, unique=True, nullable=False)

    # ✅ Fix: Use `back_populates` to correctly link to `User`
    user = relationship("User", back_populates="mapping")
