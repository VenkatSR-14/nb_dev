from sqlalchemy.orm import Session
from app.repositories.user_repository import insert_user, get_user_by_username, update_user_details
from app.models.user import User
import bcrypt
from app.services.llm_service import LLMService
from app.models.recommendations import Recommendation
from app.services.recommender.hybrid import hybrid_recommendation

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

def login_user(db: Session, username: str, password: str):
    """
    Authenticates a user and triggers the recommendation system.
    """
    user = db.query(User).filter(User.username == username).first()

    if not user or not bcrypt.checkpw(password.encode("utf-8"), user.password_hash.encode("utf-8")):
        return {"error": "Invalid credentials"}

    # ✅ Automatically generate recommendations on login
    recommendations = hybrid_recommendation(db, user.user_id, top_n=5)

    # ✅ Store recommendations in the database
    db.query(Recommendation).filter(Recommendation.user_id == user.user_id).delete()  # ✅ Clear old recommendations
    for rec in recommendations:
        db_rec = Recommendation(
            user_id=user.user_id,
            meal_id=rec.get("meal_id"),
            exercise_id=rec.get("exercise_id"),
            recommendation_reason="Generated on login"
        )
        db.add(db_rec)

    db.commit()

    # ✅ Return `user_id` along with success message
    return {
        "message": "Login successful",
        "user_id": user.user_id,  # ✅ Include user_id in the response
        "access_token": "dummy_token"  # Replace with actual JWT if implemented
    }


# Function to update user details
def update_user(db: Session, user_id: int, height: float, weight: float, disease: str, diet: str):
    return update_user_details(db, user_id, height, weight, disease, diet)
