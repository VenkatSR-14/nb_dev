import pandas as pd
import numpy as np
from sqlalchemy.orm import Session
from app.models.user import User
from app.models.meal import Meal
from app.models.recent_activity import RecentActivity

def recommend_user_based(db: Session, user_id: int, top_n=5):
    """
    Recommend meals using user-based collaborative filtering (Pearson Correlation).
    """
    # Load user ratings from the database
    meal_ratings = pd.DataFrame(db.query(RecentActivity).all(), columns=["user_id", "meal_id", "rated"])

    if user_id not in meal_ratings["user_id"].unique():
        return {"error": "User not found"}

    user_ratings = meal_ratings.pivot(index="user_id", columns="meal_id", values="rated").fillna(0)

    # Compute similarity scores
    user_similarity = user_ratings.corr(method="pearson")

    similar_users = user_similarity[user_id].sort_values(ascending=False)[1:top_n+1]

    recommended_meals = set()
    for sim_user in similar_users.index:
        user_meals = meal_ratings[meal_ratings["user_id"] == sim_user]["meal_id"].values
        recommended_meals.update(user_meals)

    return list(recommended_meals)[:top_n]
