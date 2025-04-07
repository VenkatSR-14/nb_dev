from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services.user_service import create_user, get_user_by_username, update_user, login_user
from pydantic import BaseModel
from app.services.llm_service import LLMService
from app.models.user import User
from passlib.context import CryptContext

router = APIRouter()
# Define password context at module level
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class SignupRequest(BaseModel):
    username: str
    password: str
    email: str
    veg_non: bool
    height: float
    weight: float
    disease: str
    gender: bool

class LoginRequest(BaseModel):
    username: str
    password: str

class UserProfileResponse(BaseModel):
    username: str
    email: str
    height: float
    weight: float
    diet_preference: str
    gender: str
    disease: str

class UserUpdateRequest(BaseModel):
    height: float
    weight: float
    disease: str

class ChangePasswordRequest(BaseModel):
    old_password: str
    new_password: str

@router.get("/profile/{user_id}", response_model=UserProfileResponse)
async def get_user_profile(user_id: int, db: Session = Depends(get_db)):
    """
    Fetch user profile data by user_id.
    """
    user = db.query(User).filter(User.user_id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return {
        "username": user.username,
        "email": user.email,
        "height": user.height,
        "weight": user.weight,
        "diet_preference": "vegetarian" if not user.veg_non else "non-vegetarian",
        "gender": "male" if not user.gender else "female",
        "disease": user.disease
    }

@router.post("/signup")
async def signup(user: SignupRequest, db: Session = Depends(get_db)):

    print("Received Data:", user.dict())  # ✅ Debugging
    
    db_user = get_user_by_username(db, user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already exists")
    
    # ✅ Call LLM to parse disease and recommend diet
    disease_diet_data = LLMService.process_disease_history(user.disease)
    
    parsed_diseases = ", ".join(disease_diet_data["diseases"])
    recommended_diet = disease_diet_data["recommended_diet"]

    print("Parsed Diseases:", parsed_diseases)
    print("Recommended Diet:", recommended_diet)
    
    if not parsed_diseases:
        raise HTTPException(status_code=400, detail="No diseases detected. The input may be invalid or out of scope for the current system.")

    # ✅ Insert into database with LLM-processed disease & diet
    result = create_user(
        db, user.username, user.password, user.email, user.veg_non, 
        user.height, user.weight, parsed_diseases, recommended_diet, user.gender
    )
    
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])

    return {"message": "User created successfully", "user_id": result["user_id"]}

@router.post("/login")
async def login(user: LoginRequest, db: Session = Depends(get_db)):
    """
    User login endpoint that triggers recommendations.
    """
    result = login_user(db, user.username, user.password)
    
    if "error" in result:
        raise HTTPException(status_code=401, detail=result["error"])

    return result

@router.put("/update-user/{user_id}")
async def update_user_details(user_id: int, user_update: UserUpdateRequest, db: Session = Depends(get_db)):
    # Process disease history and get recommended diet
    disease_diet_data = LLMService.process_disease_history(user_update.disease)
    
    parsed_diseases = ", ".join(disease_diet_data["diseases"])
    recommended_diet = disease_diet_data["recommended_diet"]

    if not parsed_diseases:
        raise HTTPException(status_code=400, detail="No diseases detected. The input may be invalid or out of scope for the current system.")

    # Update user with parsed diseases and recommended diet
    updated_user = update_user(db, user_id, user_update.height, user_update.weight, parsed_diseases, recommended_diet)
    
    if not updated_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return {
        "message": "User updated successfully",
        "user_id": user_id,
        "parsed_diseases": parsed_diseases,
        "recommended_diet": recommended_diet
    }


@router.put("/change-password/{user_id}")
async def change_password(user_id: int, password_data: ChangePasswordRequest, db: Session = Depends(get_db)):
    """
    Change user password endpoint.
    Requires old password verification before updating to new password.
    """
    # Find the user
    user = db.query(User).filter(User.user_id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Verify old password using passlib
    if not pwd_context.verify(password_data.old_password, user.password_hash):
        raise HTTPException(status_code=400, detail="Incorrect old password")
    
    # Update password using passlib
    user.password_hash = pwd_context.hash(password_data.new_password)
    db.commit()
    
    return {"message": "Password changed successfully"}