import pandas as pd
import numpy as np
from sqlalchemy.orm import Session
from app.models.user import User
from app.models.meal import Meal
from app.models.recent_activity import RecentActivity
import pandas as pd
import numpy as np
from sqlalchemy.orm import Session


def recommend_user_based(db: Session, user_id: int, top_n=5):
    """
    Recommend meals using user-based collaborative filtering (Pearson Correlation).
    """
    # Load user ratings from the database
    activities_query = db.query(RecentActivity).all()
    meal_ratings = pd.DataFrame(
        [activity.__dict__ for activity in activities_query], 
        columns=["user_id", "meal_id", "rated"]
    ).drop("_sa_instance_state", axis=1, errors="ignore")  # ✅ Remove SQLAlchemy instance metadata

    if user_id not in meal_ratings["user_id"].unique():
        return {"error": "User not found"}

    # Create a user-item matrix
    user_ratings = meal_ratings.pivot(index="user_id", columns="meal_id", values="rated").fillna(0)

    # ✅ Compute user similarity instead of item similarity
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


def recommend_item_based(db: Session, user_id: int, top_n=5):
    """
    Recommend meals using item-based collaborative filtering.
    """
    # Load user ratings from the database
    meal_ratings = pd.DataFrame(db.query(RecentActivity).all(), columns=["user_id", "meal_id", "rated"])

    if user_id not in meal_ratings["user_id"].unique():
        return {"error": "User not found"}

    # Create a user-item matrix
    user_ratings = meal_ratings.pivot(index="user_id", columns="meal_id", values="rated").fillna(0)

    # Compute item similarity (meal-to-meal similarity)
    item_similarity = user_ratings.T.corr().fillna(0)

    # Get meals the user has interacted with
    user_meals = meal_ratings[meal_ratings["user_id"] == user_id]["meal_id"].values

    recommended_meals = set()
    for meal in user_meals:
        similar_meals = item_similarity[meal].sort_values(ascending=False)[1:top_n+1].index
        recommended_meals.update(similar_meals)

    return list(recommended_meals)[:top_n]
