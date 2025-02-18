from sqlalchemy.orm import Session
from models.user import User
from core.security import hash_password  # Assume you have password hashing function

def create_user(db: Session, username: str, password: str, email: str, veg_non: bool, height: float, weight: float, disease: str, diet: str):
    """
    Create a new user and store in the database.
    """
    new_user = User(
        username=username,
        password_hash=hash_password(password),  # Hash the password
        email=email,
        veg_non=veg_non,
        height=height,
        weight=weight,
        disease=disease,
        diet=diet
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def get_user_by_username(db: Session, username: str):
    """
    Retrieve a user by username.
    """
    return db.query(User).filter(User.username == username).first()

def update_user(db: Session, user_id: int, height: float, weight: float, disease: str, diet: str):
    """
    Update user details.
    """
    user = db.query(User).filter(User.user_id == user_id).first()
    if user:
        user.height = height
        user.weight = weight
        user.disease = disease
        user.diet = diet
        db.commit()
        db.refresh(user)
    return user
