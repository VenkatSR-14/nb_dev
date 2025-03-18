import pandas as pd
from sqlalchemy.orm import Session
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from app.models.user import User
from app.models.meal import Meal
from app.models.recent_activity import RecentActivity

def recommend_content_based(db: Session, user_id: int, top_n=10):
    """
    Recommend meals based on a user's disease history and dietary preferences 
    using TF-IDF content-based filtering.
    """
    # Get user profile
    user = db.query(User).filter(User.user_id == user_id).first()
    
    if not user:
        return []  # Return empty list for consistency with other recommenders
    
    # Get user's preferred diet and disease history
    user_diet = user.diet if user.diet else ""
    user_disease = user.disease if user.disease else ""
    
    # Get user's existing interactions to exclude from recommendations
    user_interactions = db.query(RecentActivity).filter(
        RecentActivity.user_id == user_id
    ).all()
    
    interacted_meal_ids = set()
    for interaction in user_interactions:
        interacted_meal_ids.add(interaction.meal_id)
    
    # Load all meals from the database
    meals_query = db.query(Meal).all()
    
    # Convert to DataFrame, handling SQLAlchemy state
    meals_data = []
    for meal in meals_query:
        meal_dict = {
            "meal_id": meal.meal_id,
            "name": meal.name,
            "nutrient": meal.nutrient if meal.nutrient else "",
            "disease": meal.disease if meal.disease else "",
            "diet": meal.diet if meal.diet else ""
        }
        meals_data.append(meal_dict)
    
    meals = pd.DataFrame(meals_data)
    
    if meals.empty:
        return []  # Return empty list if no meals found
    
    # Create feature text by combining relevant attributes
    # Include all relevant features for better matching
    meals["features"] = (
        meals["nutrient"] + " " + 
        meals["disease"] + " " + 
        meals["diet"]
    ).str.lower()  # Convert to lowercase for better matching
    
    # Create user profile feature text
    user_profile = (user_diet + " " + user_disease).lower()
    
    # Handle empty user profile
    if not user_profile.strip():
        # If user has no profile, return empty list or random meals
        return []
    
    try:
        # Initialize and fit TF-IDF vectorizer
        vectorizer = TfidfVectorizer(stop_words='english')  # Remove common English words
        meal_vectors = vectorizer.fit_transform(meals["features"])
        
        # Transform user profile
        user_vector = vectorizer.transform([user_profile])
        
        # Compute cosine similarity
        similarity_scores = cosine_similarity(user_vector, meal_vectors).flatten()
        
        # Add similarity scores to meals DataFrame
        meals["similarity"] = similarity_scores
        
        # Filter out meals the user has already interacted with
        meals = meals[~meals["meal_id"].isin(interacted_meal_ids)]
        
        # Recommend top N meals with highest similarity
        recommended_meals = meals.sort_values(by="similarity", ascending=False).head(top_n)
        
        # Convert to list of dictionaries with consistent format
        result = []
        for _, meal in recommended_meals.iterrows():
            result.append({
                "meal_id": meal["meal_id"],
                "name": meal["name"],
                "nutrient": meal["nutrient"],
                "disease": meal["disease"],
                "diet": meal["diet"],
                "score": "content-based"
            })
        
        return result
    
    except Exception as e:
        print(f"Error in content-based recommendation: {str(e)}")
        return []  # Return empty list on error
