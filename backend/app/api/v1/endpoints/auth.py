# from fastapi import APIRouter, Depends, HTTPException
# from sqlalchemy.orm import Session
# from app.core.database import get_db
# from app.services.user_service import create_user
# from pydantic import BaseModel

# router = APIRouter()

# class SignUpRequest(BaseModel):
#     username: str
#     password: str
#     email: str
#     disease: str  
#     height: float
#     weight: float
#     veg_non: bool  # ✅ Correct type
#     gender: bool   # ✅ Correct type

# @router.post("/signup")
# def signup(user: SignUpRequest, db: Session = Depends(get_db)):
#     result = create_user(
#         db=db,
#         username=user.username,
#         password=user.password,
#         email=user.email,
#         veg_non=user.veg_non,
#         height=user.height,
#         weight=user.weight,
#         disease=user.disease,  # ✅ Updated to match backend logic
#         gender=user.gender
#     )
    
#     if "error" in result:
#         raise HTTPException(status_code=400, detail=result["error"])

#     return result
