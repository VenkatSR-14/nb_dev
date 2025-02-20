from app.services.recommender.content_based import recommend_content_based
from app.services.recommender.collaborative import recommend_user_based, recommend_item_based
from sqlalchemy.orm import Session

def hybrid_recommendation(db: Session, user_id, top_n=5):
    content_based = recommend_content_based(db, user_id, top_n)
    user_based = recommend_user_based(db, user_id, top_n)
    item_based = recommend_item_based(db, user_id, top_n)

    # ✅ Handle errors gracefully and ensure we return dicts
    recommendations = set()
    for rec_list in [content_based, user_based, item_based]:
        if isinstance(rec_list, list):
            for rec in rec_list:
                if isinstance(rec, dict):  # ✅ Ensure rec is a dict
                    rec_tuple = tuple(sorted(rec.items()))  # Convert dict to tuple for uniqueness
                    recommendations.add(rec_tuple)

    # ✅ Convert back to a list of dicts before returning
    return [dict(rec) for rec in recommendations] if recommendations else {"error": "No recommendations found"}
