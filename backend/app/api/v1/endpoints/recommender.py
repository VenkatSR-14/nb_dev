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
import pandas as pd
import numpy as np
router = APIRouter()


class ExerciseRecommendation(BaseModel):
    name: str
    type: str
    duration: int
    calories_burned: float
    description: str
    intensity: str
    bmi_range: str

class ExerciseRequest(BaseModel):
    height: float
    weight: float
    
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
                print(meal.veg_non)
                if meal:
                    recommendations_list.append({
                        "meal_id": meal.meal_id,
                        "name": meal.name,
                        "nutrient": meal.nutrient,
                        "disease": meal.disease,
                        "diet": meal.diet,
                        "is_vegetarian": True if meal.veg_non == 0 else False,
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

@router.post("/exercise/{user_id}")
async def recommend_exercises(user_id: int, exercise_request: ExerciseRequest, db: Session = Depends(get_db)):
    """
    Recommend exercises based on user's physical attributes using machine learning.
    """
    try:
        height = exercise_request.height
        weight = exercise_request.weight
        height_m = height / 100
        bmi = weight / (height_m ** 2)

        if bmi < 18.5:
            bmi_category = "Underweight"
        elif 18.5 <= bmi < 25:
            bmi_category = "Normal weight"
        elif 25 <= bmi < 30:
            bmi_category = "Overweight"
        else:
            bmi_category = "Obese"

        # Load exercise data using pd.read_csv
        try:
            exercise_df = pd.read_csv("/app/data/cleaned/cleaned_exercise.csv")
        except FileNotFoundError:
            raise HTTPException(status_code=500, detail="Exercise data file not found")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error loading exercise data: {str(e)}")


        from sklearn.ensemble import RandomForestRegressor
        from sklearn.preprocessing import StandardScaler

        # Train model - Correct the column names to match the exercise dataset
        X_train = exercise_df[["bmi"]]
        y_train = exercise_df["exercise_intensity"]

        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)

        model = RandomForestRegressor(n_estimators=100, random_state=42)
        model.fit(X_train_scaled, y_train)

        user_features = np.array([[bmi]])
        user_features_scaled = scaler.transform(user_features)
        predicted_intensity = model.predict(user_features_scaled)[0]

        feature_importance = model.feature_importances_

        intensity_range = (max(0, predicted_intensity - 1), min(10, predicted_intensity + 1))

        # Filter exercises based on the predicted intensity range
        filtered_exercises = exercise_df[
            exercise_df['exercise_intensity'].between(intensity_range[0], intensity_range[1])
        ]

        if len(filtered_exercises) < 5:
            intensity_range = (max(0, predicted_intensity - 2), min(10, predicted_intensity + 2))
            filtered_exercises = exercise_df[
                exercise_df['exercise_intensity'].between(intensity_range[0], intensity_range[1])
            ]

        exercise_types = filtered_exercises['exercise'].unique()
        recommended_exercises = pd.DataFrame()

        for exercise_type in exercise_types:
            type_exercises = filtered_exercises[filtered_exercises['exercise'] == exercise_type]
            if not type_exercises.empty:
                type_exercises['intensity_diff'] = abs(type_exercises['exercise_intensity'] - predicted_intensity)
                type_exercises = type_exercises.sort_values('intensity_diff').head(2)
                recommended_exercises = pd.concat([recommended_exercises, type_exercises])

        recommended_exercises = recommended_exercises.head(5)

        exercise_list = []
        for _, exercise in recommended_exercises.iterrows():
            exercise_info = {
                "name": exercise['exercise'],
                "type": "Not available",
                "duration": int(exercise['duration']),
                "calories_burned": float(exercise['calories_burn']),
                "description": "Not available",
                "intensity": str(exercise['exercise_intensity']),
                "bmi_range": bmi_category,
                "match_score": float(100 - (exercise['intensity_diff'] * 10)) if 'intensity_diff' in exercise else 95.0
            }
            exercise_list.append(exercise_info)

        exercise_recommendations = [ExerciseRecommendation(**exercise) for exercise in exercise_list]

        return {
            "bmi": bmi,
            "bmi_category": bmi_category,
            "predicted_intensity": float(predicted_intensity),
            "feature_importance": {
                "bmi": float(feature_importance[0])
            },
            "recommendations": exercise_recommendations
        }
    except Exception as e:
        print(f"Error recommending exercises: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error recommending exercises: {str(e)}")
    
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

@router.post("/rerun-recommendations/{user_id}")
async def rerun_recommendations(
    user_id: int,
    db: Session = Depends(get_db)
):
    """
    Reruns both exercise and meal recommendations for the user after profile updates.
    """
    try:
        # Fetch user data
        user = db.query(User).filter(User.user_id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        # Rerun meal recommendations
        meal_recommendations = hybrid_recommendation(db, user_id, top_n=10)
        if isinstance(meal_recommendations, dict) and "error" in meal_recommendations:
            raise HTTPException(status_code=500, detail=meal_recommendations["error"])

        # Store meal recommendations in the database
        store_recommendations(db, user_id, meal_recommendations)

        # Create exercise request with updated user data
        exercise_request = ExerciseRequest(
            height=user.height,
            weight=user.weight
        )
        
        # Rerun exercise recommendations
        exercise_recommendations = await recommend_exercises(
            user_id=user_id, 
            exercise_request=exercise_request, 
            db=db
        )

        return {
            "message": "Recommendations refreshed successfully!",
            "meal_recommendations": meal_recommendations,
            "exercise_recommendations": exercise_recommendations["recommendations"]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to rerun recommendations: {str(e)}")
