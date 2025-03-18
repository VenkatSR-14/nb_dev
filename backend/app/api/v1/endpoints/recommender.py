from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.recent_activity import RecentActivity
from app.services.recommender.hybrid import hybrid_recommendation
from pydantic import BaseModel
from app.models.user import User
from app.models.recommendations import Recommendation  # Fixed model name
from app.models.meal import Meal
from datetime import datetime, timedelta

router = APIRouter()

@router.get("/recommend/{user_id}")
async def recommend_meals(user_id: int, top_n: int = 10, refresh: bool = False, db: Session = Depends(get_db)):
    """
    Returns hybrid recommendations for meals, considering:
    1️⃣ Content-Based Filtering
    2️⃣ Collaborative Filtering
    3️⃣ Global & Similar-User Popularity-Based Recommendations
    
    If refresh=True, forces regeneration of recommendations
    """
    # Check if we have recent recommendations stored (less than 24 hours old)
    recent_time = datetime.utcnow() - timedelta(hours=24)
    
    # Only use stored recommendations if not forcing refresh
    if not refresh:
        stored_recommendations = db.query(Recommendation).filter(
            Recommendation.user_id == user_id,
            Recommendation.created_at > recent_time
        ).all()
        
        if stored_recommendations:
    # Format stored recommendations
            recommendations_list = []
            for rec in stored_recommendations:
                meal = db.query(Meal).filter(Meal.meal_id == rec.meal_id).first()
                if meal:
                    recommendations_list.append({
                        "meal_id": meal.meal_id,
                        "name": meal.name,
                        "nutrient": meal.nutrient,
                        "disease": meal.disease,
                        "diet": meal.diet,
                        "is_vegetarian": "vegetarian" in meal.diet.lower() if meal.diet else False,
                        "reason": rec.recommendation_reason
                    })
            
            return {"user_id": user_id, "recommendations": recommendations_list}

            
    # Generate fresh recommendations
    recommendations = hybrid_recommendation(db, user_id, top_n)
    
    if isinstance(recommendations, dict) and "error" in recommendations:
        raise HTTPException(status_code=404, detail=recommendations["error"])
    
    # Store the new recommendations
    store_recommendations(db, user_id, recommendations)
    
    return {"user_id": user_id, "recommendations": recommendations}


# ✅ Define Pydantic model to accept JSON body
class InteractionRequest(BaseModel):
    user_id: int
    meal_id: int
    action: str
    rating: int | None = None

@router.post("/interact")
async def interact_with_meal(
    request: InteractionRequest, 
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """
    Logs user interactions (like, dislike, purchase, and rating) with meals.
    After interaction, triggers recommendations for users with similar disease history.
    """
    valid_actions = ["like", "dislike", "buy", "rate"]
    if request.action not in valid_actions:
        raise HTTPException(status_code=400, detail="Invalid action. Choose from 'like', 'dislike', 'buy', or 'rate'.")

    # Get the current user's disease history
    user = db.query(User).filter(User.user_id == request.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Check if user already interacted with the meal
    existing_activity = db.query(RecentActivity).filter(
        RecentActivity.user_id == request.user_id,
        RecentActivity.meal_id == request.meal_id
    ).first()

    if not existing_activity:
        # Create a new entry if interaction doesn't exist
        existing_activity = RecentActivity(
            user_id=request.user_id,
            meal_id=request.meal_id,
            liked=True if request.action == "like" else False,
            purchased=True if request.action == "buy" else False,
            rated=True if request.action == "rate" else False,
            timestamp=datetime.now()
        )
        db.add(existing_activity)
    else:
        # Update existing entry based on action
        if request.action == "like":
            existing_activity.liked = True
        elif request.action == "dislike":
            existing_activity.liked = False
        elif request.action == "buy":
            existing_activity.purchased = True
        elif request.action == "rate" and request.rating is not None:
            existing_activity.rated = True
        
        existing_activity.timestamp = datetime.now()

    db.commit()

    # Update recommendations for the current user
    recommendations = hybrid_recommendation(db, request.user_id)
    for rec in recommendations:
        if "is_vegetarian" not in rec and "diet" in rec:
            rec["is_vegetarian"] = "vegetarian" in rec["diet"].lower() if rec["diet"] else False
    store_recommendations(db, request.user_id, recommendations)
    
    # Update recommendations for users with similar disease history in the background
    background_tasks.add_task(
        update_recommendations_for_similar_users, 
        db=db, 
        user_id=request.user_id, 
        user_disease=user.disease
    )

    return {"message": f"Meal {request.meal_id} {request.action}d successfully!", "action": request.action}

def store_recommendations(db: Session, user_id: int, recommendations: list):
    """
    Store recommendations in the database
    """
    try:
        # Clear existing recommendations for the user
        db.query(Recommendation).filter(Recommendation.user_id == user_id).delete()
        
        # Store new recommendations
        for rec in recommendations:
            meal_id = rec["meal_id"]
            
            new_recommendation = Recommendation(
                user_id=user_id,
                meal_id=meal_id,
                recommendation_reason="Based on your preferences and similar users",
                created_at=datetime.utcnow()
            )
            db.add(new_recommendation)
        
        db.commit()
    except Exception as e:
        db.rollback()
        print(f"Error storing recommendations for user {user_id}: {str(e)}")

def update_recommendations_for_similar_users(db: Session, user_id: int, user_disease: str):
    """
    Background task to update recommendations for users with similar disease history.
    """
    # Find users with similar disease history
    similar_users = db.query(User).filter(
        User.user_id != user_id,  # Exclude the current user
        User.disease == user_disease  # Match the exact disease
    ).all()
    
    # Add the current user to the list to update their recommendations too
    current_user = db.query(User).filter(User.user_id == user_id).first()
    if current_user:
        similar_users.append(current_user)
    
    # Generate new recommendations for each similar user
    for similar_user in similar_users:
        try:
            # Generate recommendations using the hybrid recommender
            recommendations = hybrid_recommendation(db, similar_user.user_id)
            
            # Store the recommendations
            store_recommendations(db, similar_user.user_id, recommendations)
            
            print(f"Updated recommendations for user {similar_user.user_id} with disease {user_disease}")
        except Exception as e:
            print(f"Error updating recommendations for user {similar_user.user_id}: {str(e)}")


# Add a new endpoint to refresh recommendations on login
@router.post("/refresh-recommendations/{user_id}")
async def refresh_user_recommendations(
    user_id: int,
    db: Session = Depends(get_db)
):
    """
    Refreshes recommendations for a user, typically called after login
    """
    try:
        # Generate fresh recommendations
        recommendations = hybrid_recommendation(db, user_id)
        
        # Store the recommendations
        store_recommendations(db, user_id, recommendations)
        
        return {"message": "Recommendations refreshed successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to refresh recommendations: {str(e)}")
