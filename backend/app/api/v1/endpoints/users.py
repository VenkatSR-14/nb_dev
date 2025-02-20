from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services.user_service import create_user, get_user_by_username, update_user, login_user
from pydantic import BaseModel
from app.services.llm_service import LLMService

router = APIRouter()

class SignupRequest(BaseModel):
    username: str
    password: str
    email: str
    veg_non: bool
    height: float
    weight: float
    disease: str
    gender: bool  # ✅ Ensure this is included

class LoginRequest(BaseModel):
    username: str
    password: str

@router.post("/signup")
async def signup(user: SignupRequest, db: Session = Depends(get_db)):
    print("Here!")
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
async def update_user_details(user_id: int, user: SignupRequest, db: Session = Depends(get_db)):
    updated_user = update_user(db, user_id, user.height, user.weight, user.disease, user.diet)
    if not updated_user:
        raise HTTPException(status_code=404, detail="User not found")
    return updated_user
