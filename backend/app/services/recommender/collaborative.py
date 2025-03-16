import pandas as pd
import numpy as np
from sqlalchemy.orm import Session
from app.models.recent_activity import RecentActivity

def recommend_user_based(db: Session, user_id: int, top_n=10):
    """
    Recommend meals using user-based collaborative filtering (Pearson Correlation).
    """
    # ✅ Load user ratings from the database and aggregate to avoid duplicates
    activities_query = db.query(RecentActivity).all()
    
    meal_ratings = pd.DataFrame(
        [{"user_id": activity.user_id, "meal_id": activity.meal_id, "rated": int(activity.rated)} for activity in activities_query]
    )

    if meal_ratings.empty:
        return {"error": "No recent activity found."}

    if user_id not in meal_ratings["user_id"].unique():
        return {"error": "User not found"}

    # ✅ Aggregate ratings to prevent duplicates (take the max rating if multiple exist)
    meal_ratings = meal_ratings.groupby(["user_id", "meal_id"], as_index=False).max()

    # ✅ Create a user-item matrix
    user_ratings = meal_ratings.pivot(index="user_id", columns="meal_id", values="rated").fillna(0)

    # ✅ Compute user similarity
    user_similarity = user_ratings.corr(method="pearson").fillna(0)

    if user_id not in user_similarity.index:
        return {"error": "User not found in similarity matrix"}

    # Find similar users
    similar_users = user_similarity[user_id].sort_values(ascending=False)[1:top_n+1]

    recommended_meals = set()
    for sim_user in similar_users.index:
        user_meals = meal_ratings[meal_ratings["user_id"] == sim_user]["meal_id"].values
        recommended_meals.update(user_meals)

    return list(recommended_meals)[:top_n]


def recommend_item_based(db: Session, user_id: int, top_n=10):
    """
    Recommend meals using item-based collaborative filtering.
    """
    # ✅ Load user ratings from the database
    activities_query = db.query(RecentActivity).all()
    
    # ✅ Convert ORM objects into a DataFrame properly
    meal_ratings = pd.DataFrame(
        [{"user_id": activity.user_id, "meal_id": activity.meal_id, "rated": int(activity.rated)} for activity in activities_query]
    )

    if meal_ratings.empty:
        return {"error": "No recent activity found."}

    if user_id not in meal_ratings["user_id"].unique():
        return {"error": "User not found"}

    # ✅ Aggregate ratings to prevent duplicates
    meal_ratings = meal_ratings.groupby(["user_id", "meal_id"], as_index=False).max()

    # ✅ Create a user-item matrix
    user_ratings = meal_ratings.pivot(index="user_id", columns="meal_id", values="rated").fillna(0)

    # ✅ Compute item similarity (meal-to-meal similarity)
    item_similarity = user_ratings.T.corr().fillna(0)

    # ✅ Get meals the user has interacted with
    user_meals = meal_ratings[meal_ratings["user_id"] == user_id]["meal_id"].values

    recommended_meals = set()
    for meal in user_meals:
        if meal in item_similarity:
            similar_meals = item_similarity[meal].sort_values(ascending=False)[1:top_n+1].index
            recommended_meals.update(similar_meals)

    return list(recommended_meals)[:top_n]
