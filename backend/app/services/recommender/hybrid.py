from app.services.recommender.content_based import recommend_content_based
from app.services.recommender.collaborative import recommend_user_based, recommend_item_based
from sqlalchemy.orm import Session
from app.models.recent_activity import RecentActivity
from app.models.user import User
from app.models.meal import Meal
from collections import Counter

def hybrid_recommendation(db: Session, user_id, top_n=15):
    """
    Combines Content-Based, Collaborative, and Popularity-Based recommendations.
    Prioritizes meals that multiple users (with similar conditions) have liked.
    """

    user = db.query(User).filter(User.user_id == user_id).first()
    if not user:
        return {"error": "User not found"}

    # ✅ Fetch users with the same condition
    similar_users = db.query(User).filter(User.disease == user.disease).all()
    similar_user_ids = [u.user_id for u in similar_users]

    # ✅ Track meals based on popularity across ALL users (not just similar)
    global_liked_meal_counts = Counter(
        activity.meal_id
        for activity in db.query(RecentActivity)
        .filter(RecentActivity.liked == True)
        .all()
    )

    # ✅ Track most liked meals by similar users
    similar_liked_meal_counts = Counter(
        activity.meal_id
        for activity in db.query(RecentActivity)
        .filter(RecentActivity.user_id.in_(similar_user_ids), RecentActivity.liked == True)
        .all()
    )

    # ✅ Get standard recommendations
    content_based = recommend_content_based(db, user_id, top_n * 2)
    user_based = recommend_user_based(db, user_id, top_n * 2)
    item_based = recommend_item_based(db, user_id, top_n * 2)

    # ✅ Merge & rank recommendations
    recommendations = []
    meal_priority = {}

    for rec_list in [content_based, user_based, item_based]:
        if isinstance(rec_list, list):
            for rec in rec_list:
                if isinstance(rec, dict):
                    meal_id = rec["meal_id"]

                    # ✅ Assign priority based on likes by **all users** and **similar users**
                    priority = global_liked_meal_counts.get(meal_id, 0) * 3  # Global impact
                    priority += similar_liked_meal_counts.get(meal_id, 0) * 5  # Personal impact

                    # ✅ Boost meals the user has already liked
                    if db.query(RecentActivity).filter_by(user_id=user_id, meal_id=meal_id, liked=True).first():
                        priority += 10  # Increase priority for the same user

                    meal_priority[meal_id] = priority
                    recommendations.append(rec)

    # Add this code right here
    # Boost meals that are popular among users with the same disease
    for meal_id, count in similar_liked_meal_counts.most_common(5):  # Top 5 most popular meals
        if meal_id in meal_priority:
            meal_priority[meal_id] += 25  # Give high priority to disease-specific popular meals

    # ✅ Sort recommendations by popularity & personal preference
    recommendations.sort(key=lambda r: meal_priority.get(r["meal_id"], 0), reverse=True)

    user_liked_meals = db.query(RecentActivity).filter_by(user_id=user_id, liked=True).all()

# After your initial recommendations are sorted
# Add user's liked/purchased meals to the top if not already included
    user_liked_meal_ids = [activity.meal_id for activity in user_liked_meals]
    for meal_id in user_liked_meal_ids:
        if meal_id not in [r["meal_id"] for r in recommendations]:
            meal = db.query(Meal).filter(Meal.meal_id == meal_id).first()
            if meal:
                recommendations.insert(0, {
                    "meal_id": meal.meal_id,
                    "name": meal.name,
                    "nutrient": meal.nutrient,
                    "disease": meal.disease,
                    "diet": meal.diet,
                    "source": "previously-liked"
                })

    # ✅ Ensure at least 10 meals are in recommendations
    if len(recommendations) < 10:
        missing_count = 10 - len(recommendations)
        additional_meals = db.query(Meal).filter(
            Meal.meal_id.notin_([r["meal_id"] for r in recommendations])
        ).limit(missing_count).all()

    return recommendations
