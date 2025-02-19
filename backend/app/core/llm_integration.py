import openai
import pandas as pd
from typing import List, Dict, Optional
from app.core.config import settings
import ast

# ✅ Initialize OpenAI client (New API format)
client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)

# Load preprocessed files
DIET_FILE_PATH = "data/cleaned/cleaned_meals.csv"
USER_PROFILES_PATH = "data/cleaned/cleaned_user_profiles.csv"

# Load valid diseases from the user profile dataset
user_profiles = pd.read_csv(USER_PROFILES_PATH)
valid_diseases = set()

for diseases in user_profiles["Disease"].dropna():
    for disease in diseases.split():
        valid_diseases.add(disease.strip())

def parse_disease_history(history: str, img_url: Optional[str] = None) -> List[str]:
    """
    Uses GPT-3.5-Turbo to extract diseases ONLY from the preprocessed user profile dataset.
    Supports both text and optional image input.
    """
    if not history.strip():
        return []  # ✅ Handle empty history input gracefully

    valid_diseases_str = ", ".join(valid_diseases)

    prompt = (
        f"Extract diseases from the following medical history:\n\n{history}\n\n"
        f"Return all the applicable diseases in this list: {valid_diseases_str}.\n"
        f"Return diseases as a comma-separated format."
    )

    try:
        messages = [{"role": "user", "content": prompt}]

        if img_url:
            messages.append({"role": "user", "content": {"type": "image_url", "image_url": {"url": img_url}}})

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",  # ✅ Using GPT-3.5-Turbo
            messages=messages
        )

        diseases = response.choices[0].message.content.strip()
        print(diseases)
        if not diseases:
            return []  # ✅ Ensure a response is always returned

        parsed_diseases = [d.strip() for d in diseases.split(",") if d.strip() in valid_diseases]

        return parsed_diseases if parsed_diseases else []
    
    except Exception as e:
        print("Error calling OpenAI:", e)
        return []  # ✅ Prevent crashes if OpenAI API fails


# Load preprocessed diet dataset
disease_diet_map = pd.read_csv(DIET_FILE_PATH)

def recommend_diet(diseases: List[str]) -> str:
    """
    Matches extracted diseases to recommended diets based on the preprocessed dataset.
    If no match is found, queries GPT-3.5-Turbo for a dynamic recommendation.
    """
    matched_diets = set()

    for disease in diseases:
        matching_rows = disease_diet_map[disease_diet_map["Disease"].str.contains(disease, case=False, na=False)]
    
        for diet_list in matching_rows["Diet"]:
            # Convert the string representation of a list into an actual Python list
            parsed_diets = ast.literal_eval(diet_list) if isinstance(diet_list, str) else diet_list
            matched_diets.update(parsed_diets)  # Add individual diets to the set
        
    if matched_diets:
        
        unique_diets = sorted(matched_diets)

        return ", ".join(unique_diets)

    # If no predefined diet is found, ask GPT-3.5-Turbo for a recommendation
    llm_prompt = f"Suggest a suitable diet for someone with the following condition(s): {', '.join(diseases)}."

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",  # ✅ Using GPT-3.5-Turbo
            messages=[
                {"role": "system", "content": "You are a nutrition expert providing evidence-based diet recommendations."},
                {"role": "user", "content": llm_prompt}
            ]
        )
        return response.choices[0].message.content.strip()
    
    except Exception as e:
        print("Error calling OpenAI for diet recommendation:", e)
        return "No specific diet recommendation available."

def parse_disease_and_recommend_diet(history: str, img_url: Optional[str] = None) -> Dict:
    """
    Extracts diseases and recommends a diet based on validated disease list.
    Supports optional image input.
    """
    diseases = parse_disease_history(history, img_url)
    recommended_diet = recommend_diet(diseases)

    return {
        "diseases": diseases,
        "recommended_diet": recommended_diet
    }
