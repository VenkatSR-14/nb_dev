from sqlalchemy.orm import Session
from app.repositories.user_repository import insert_user, get_user_by_username, update_user_details
from app.models.user import User
import bcrypt
from app.services.llm_service import LLMService

# Function to hash password
def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode("utf-8"), salt).decode("utf-8")

# Business Logic for creating a user
def create_user(
    db: Session,
    username: str,
    password: str,
    email: str,
    veg_non: bool,
    height: float,
    weight: float,
    disease: str,
    diet: str,
    gender: bool
):
    existing_user = get_user_by_username(db, username)
    if existing_user:
        return {"error": "Username or Email already exists"}


    # ✅ Hash password only if user doesn't exist
    hashed_password = hash_password(password)

    return insert_user(db, username, hashed_password, email, veg_non, height, weight, disease, diet, gender)


# Function to update user details
def update_user(db: Session, user_id: int, height: float, weight: float, disease: str, diet: str):
    return update_user_details(db, user_id, height, weight, disease, diet)
