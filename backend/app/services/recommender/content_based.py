import pandas as pd
from sqlalchemy.orm import Session
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from app.models.user import User  # ✅ Import User model
from app.models.meal import Meal  # ✅ Import Meal model

def recommend_content_based(db: Session, user_id: int, top_n=10):
    """
    Recommend meals based on a user's preferences using TF-IDF content-based filtering.
    """
    user = db.query(User).filter(User.user_id == user_id).first()
    
    if not user:
        return {"error": "User not found"}

    preferred_nutrient = user.diet  # ✅ Fetch from DB
    preferred_diseases = user.disease   # ✅ Fetch from DB

    # Load meals from the database
    meals_query = db.query(Meal).all()
    meals = pd.DataFrame(
        [meal.__dict__ for meal in meals_query], 
        columns=["meal_id", "name", "nutrient", "disease", "diet"]
    ).drop("_sa_instance_state", axis=1, errors="ignore")  # ✅ Remove SQLAlchemy instance metadata
    
    if meals.empty:
        return {"error": "No meals found"}

    # Combine features
    meals["features"] = meals["nutrient"] + " " + meals["disease"]
    
    vectorizer = TfidfVectorizer()
    meal_vectors = vectorizer.fit_transform(meals["features"])

    user_vector = vectorizer.transform([preferred_nutrient + " " + preferred_diseases])

    # Compute cosine similarity
    similarity_scores = cosine_similarity(user_vector, meal_vectors).flatten()

    meals["similarity"] = similarity_scores

    # Recommend top N meals
    recommended_meals = meals.sort_values(by="similarity", ascending=False).head(top_n)

    return recommended_meals[["meal_id", "name", "nutrient", "disease", "diet"]].to_dict(orient="records")
