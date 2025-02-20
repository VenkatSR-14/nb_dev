from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services.recommender.hybrid import hybrid_recommendation

router = APIRouter()

@router.get("/recommend/{user_id}")
async def recommend_meals(user_id: int, top_n: int = 5, db: Session = Depends(get_db)):
    """
    Hybrid recommendation for meals & exercises using database.
    """
    recommendations = hybrid_recommendation(db, user_id, top_n)
    return {"user_id": user_id, "recommendations": recommendations}
