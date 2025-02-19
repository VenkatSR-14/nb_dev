from sqlalchemy.orm import Session
from app.models.user import User
from app.models.user_mapping import UserMapping

# Function to insert a new user
def insert_user(
    db: Session,
    username: str,
    password_hash: str,
    email: str,
    veg_non: bool,
    height: float,
    weight: float,
    disease: str,
    diet: str,
    gender: bool
):
    new_user = User(
        username=username,
        password_hash=password_hash,
        email=email,
        veg_non=veg_non,
        height=height,
        weight=weight,
        disease=disease,
        diet=diet,
        gender=gender
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # Insert into user_mapping
    user_mapping = UserMapping(user_id=new_user.user_id, username=username)
    db.add(user_mapping)
    db.commit()

    return {"message": "User created successfully", "user_id": new_user.user_id}

# Function to retrieve a user by username
def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()

# Function to update user details
def update_user_details(db: Session, user_id: int, height: float, weight: float, disease: str, diet: str):
    user = db.query(User).filter(User.user_id == user_id).first()
    if user:
        user.height = height
        user.weight = weight
        user.disease = disease
        user.diet = diet
        db.commit()
        db.refresh(user)
    return user
