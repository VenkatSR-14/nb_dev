from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.recent_activity import RecentActivity
from app.services.recommender.hybrid import hybrid_recommendation
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

router = APIRouter()

@router.get("/recommend/{user_id}")
async def recommend_meals(user_id: int, top_n: int = 10, db: Session = Depends(get_db)):
    """
    Returns hybrid recommendations for meals, considering:
    1️⃣ Content-Based Filtering
    2️⃣ Collaborative Filtering
    3️⃣ Global & Similar-User Popularity-Based Recommendations
    """
    recommendations = hybrid_recommendation(db, user_id, top_n)

    if "error" in recommendations:
        raise HTTPException(status_code=404, detail=recommendations["error"])

    return {"user_id": user_id, "recommendations": recommendations}



# ✅ Define Pydantic model to accept JSON body
class InteractionRequest(BaseModel):
    user_id: int
    meal_id: int
    action: str
    rating: int | None = None

@router.post("/interact")
async def interact_with_meal(request: InteractionRequest, db: Session = Depends(get_db)):
    """
    Logs user interactions (like, dislike, purchase, and rating) with meals.
    """
    valid_actions = ["like", "dislike", "buy", "rate"]
    if request.action not in valid_actions:
        raise HTTPException(status_code=400, detail="Invalid action. Choose from 'like', 'dislike', 'buy', or 'rate'.")

    # ✅ Check if user already interacted with the meal
    existing_activity = db.query(RecentActivity).filter(
        RecentActivity.user_id == request.user_id,
        RecentActivity.meal_id == request.meal_id
    ).first()

    if not existing_activity:
        # ✅ Create a new entry if interaction doesn't exist
        existing_activity = RecentActivity(
            user_id=request.user_id,
            meal_id=request.meal_id,
            liked=True if request.action == "like" else False,
            purchased=True if request.action == "buy" else False,
            rated=True if request.action == "rate" else False
        )
        db.add(existing_activity)
    else:
        # ✅ Update existing entry based on action
        if request.action == "like":
            existing_activity.liked = True
        elif request.action == "dislike":
            existing_activity.liked = False  # ✅ Disliked meals should not be recommended
        elif request.action == "buy":
            existing_activity.purchased = True
        elif request.action == "rate" and request.rating is not None:
            existing_activity.rated = True  # ✅ Store rating interaction

    db.commit()

    return {"message": f"Meal {request.meal_id} {request.action}d successfully!", "action": request.action}
