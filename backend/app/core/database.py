from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import settings

# Database URL
DATABASE_URL = settings.DATABASE_URL  # Load from settings

# Create SQLAlchemy Engine
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base Model
Base = declarative_base()

# Dependency for getting DB Session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
