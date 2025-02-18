from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from core.database import get_db
from services.user_service import create_user, get_user_by_username, update_user
from pydantic import BaseModel

router = APIRouter()

class SignupRequest(BaseModel):
    username: str
    password: str
    email: str
    veg_non: bool
    height: float
    weight: float
    disease: str
    diet: str

@router.post("/signup")
async def signup(user: SignupRequest, db: Session = Depends(get_db)):
    db_user = get_user_by_username(db, user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already exists")
    
    return create_user(db, user.username, user.password, user.email, user.veg_non, user.height, user.weight, user.disease, user.diet)

@router.put("/update-user/{user_id}")
async def update_user_details(user_id: int, user: SignupRequest, db: Session = Depends(get_db)):
    updated_user = update_user(db, user_id, user.height, user.weight, user.disease, user.diet)
    if not updated_user:
        raise HTTPException(status_code=404, detail="User not found")
    return updated_user
