import pandas as pd
import numpy as np
from sqlalchemy.orm import Session
from app.models.recent_activity import RecentActivity
from app.models.meal import Meal

def recommend_user_based(db: Session, user_id: int, top_n=10):
    """
    Recommend meals using user-based collaborative filtering (Pearson Correlation).
    """
    # ✅ Load user interactions from the database
    activities_query = db.query(RecentActivity).all()
    
    # Create a DataFrame with user interactions
    # Consider liked and purchased as positive signals (value 1)
    interactions = []
    for activity in activities_query:
        # Create an interaction score based on user actions
        score = 0
        if activity.liked:
            score += 1
        if activity.purchased:
            score += 1
        if activity.rated:
            score += 1
        
        if score > 0:  # Only include positive interactions
            interactions.append({
                "user_id": activity.user_id, 
                "meal_id": activity.meal_id, 
                "score": score
            })
    
    meal_ratings = pd.DataFrame(interactions)

    if meal_ratings.empty:
        return []  # Return empty list instead of error dict for consistency

    # Check if user exists in the dataset
    if user_id not in meal_ratings["user_id"].unique():
        return []  # Return empty list if user not found

    # ✅ Aggregate interactions to prevent duplicates (take the max score if multiple exist)
    meal_ratings = meal_ratings.groupby(["user_id", "meal_id"], as_index=False)["score"].max()

    # ✅ Create a user-item matrix
    try:
        user_ratings = meal_ratings.pivot(index="user_id", columns="meal_id", values="score").fillna(0)
    except ValueError:
        return []  # Handle pivot error gracefully
    
    # ✅ Compute user similarity
    try:
        user_similarity = user_ratings.corr(method="pearson").fillna(0)
    except Exception:
        return []  # Handle correlation error gracefully

    if user_id not in user_similarity.index:
        return []  # Return empty list if user not in similarity matrix

    # Find similar users (exclude self-similarity)
    similar_users = user_similarity[user_id].sort_values(ascending=False)
    if len(similar_users) > 1:
        similar_users = similar_users[1:min(len(similar_users), top_n+1)]
    else:
        return []  # No similar users found
    
    # Get user's existing interactions to exclude from recommendations
    user_interacted_meals = set(meal_ratings[meal_ratings["user_id"] == user_id]["meal_id"].values)
    
    # Collect recommendations from similar users
    recommended_meals = []
    for sim_user, similarity in similar_users.items():
        if similarity <= 0:  # Skip users with non-positive similarity
            continue
            
        # Get meals that similar user interacted with
        sim_user_meals = meal_ratings[meal_ratings["user_id"] == sim_user]["meal_id"].values
        
        # Add meals that user hasn't interacted with yet
        for meal_id in sim_user_meals:
            if meal_id not in user_interacted_meals:
                meal = db.query(Meal).filter(Meal.meal_id == meal_id).first()
                if meal:
                    recommended_meals.append({
                        "meal_id": meal_id,
                        "name": meal.name,
                        "nutrient": meal.nutrient,
                        "disease": meal.disease,
                        "diet": meal.diet,
                        "score": "user-based"
                    })
                    user_interacted_meals.add(meal_id)  # Avoid duplicate recommendations
    
    # Return top N unique recommendations
    return recommended_meals[:top_n]


def recommend_item_based(db: Session, user_id: int, top_n=10):
    """
    Recommend meals using item-based collaborative filtering.
    """
    # ✅ Load user interactions from the database
    activities_query = db.query(RecentActivity).all()
    
    # Create a DataFrame with user interactions
    interactions = []
    for activity in activities_query:
        # Create an interaction score based on user actions
        score = 0
        if activity.liked:
            score += 1
        if activity.purchased:
            score += 1
        if activity.rated:
            score += 1
        
        if score > 0:  # Only include positive interactions
            interactions.append({
                "user_id": activity.user_id, 
                "meal_id": activity.meal_id, 
                "score": score
            })
    
    meal_ratings = pd.DataFrame(interactions)

    if meal_ratings.empty:
        return []  # Return empty list instead of error dict

    # Check if user exists in the dataset
    if user_id not in meal_ratings["user_id"].unique():
        return []  # Return empty list if user not found

    # ✅ Aggregate interactions to prevent duplicates
    meal_ratings = meal_ratings.groupby(["user_id", "meal_id"], as_index=False)["score"].max()

    # ✅ Create a user-item matrix
    try:
        user_ratings = meal_ratings.pivot(index="user_id", columns="meal_id", values="score").fillna(0)
    except ValueError:
        return []  # Handle pivot error gracefully

    # ✅ Compute item similarity (meal-to-meal similarity)
    try:
        item_similarity = user_ratings.T.corr(method="pearson").fillna(0)
    except Exception:
        return []  # Handle correlation error gracefully

    # ✅ Get meals the user has interacted with
    user_meals = meal_ratings[meal_ratings["user_id"] == user_id]["meal_id"].values
    
    if len(user_meals) == 0:
        return []  # User hasn't interacted with any meals
    
    # Get user's existing interactions to exclude from recommendations
    user_interacted_meals = set(user_meals)
    
    # Calculate recommendation scores for each meal
    meal_scores = {}
    for meal_id in user_meals:
        if meal_id in item_similarity.index:
            # Get similar meals
            similar_meals = item_similarity[meal_id].sort_values(ascending=False)
            
            # Skip the meal itself (perfect correlation of 1.0)
            if len(similar_meals) > 1:
                similar_meals = similar_meals[1:]
            
            # Add similarity scores to meal_scores
            for sim_meal_id, similarity in similar_meals.items():
                if similarity <= 0 or sim_meal_id in user_interacted_meals:
                    continue
                    
                if sim_meal_id not in meal_scores:
                    meal_scores[sim_meal_id] = 0
                
                # Add weighted similarity score
                meal_scores[sim_meal_id] += similarity
    
    # Sort meals by score
    sorted_meals = sorted(meal_scores.items(), key=lambda x: x[1], reverse=True)
    
    # Get meal details for top recommendations
    recommended_meals = []
    for meal_id, score in sorted_meals[:top_n]:
        meal = db.query(Meal).filter(Meal.meal_id == meal_id).first()
        if meal:
            recommended_meals.append({
                "meal_id": meal_id,
                "name": meal.name,
                "nutrient": meal.nutrient,
                "disease": meal.disease,
                "diet": meal.diet,
                "score": "item-based"
            })
    
    return recommended_meals
