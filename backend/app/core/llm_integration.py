import openai
import pandas as pd
from typing import List, Dict
from config import settings

# Load OpenAI API Key
openai.api_key = settings.OPENAI_API_KEY

# Load preprocessed files
DIET_FILE_PATH = "data/cleaned/cleaned_meals.csv"
USER_PROFILES_PATH = "data/cleaned/cleaned_user_profiles.csv"

# Load valid diseases from the user profile dataset
user_profiles = pd.read_csv(USER_PROFILES_PATH)
valid_diseases = set()  # Store all valid diseases

# Extract diseases from CSV and clean them
for diseases in user_profiles["Disease"].dropna():
    for disease in diseases.split():
        valid_diseases.add(disease.strip())

def parse_disease_history(history: str) -> List[str]:
    """
    Uses GPT-3.5-Turbo to extract diseases ONLY from the preprocessed user profile dataset.
    Returns a list of extracted diseases.
    """
    valid_diseases_str = ", ".join(valid_diseases)  # Convert set to a string

    prompt = (
        f"Extract diseases from the following medical history:\n\n{history}\n\n"
        f"Return ONLY the diseases that are in this list: {valid_diseases_str}.\n"
        f"Return diseases in a comma-separated format."
    )

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # ✅ Using a cheaper, optimized model
            messages=[
                {"role": "system", "content": "You are a medical expert."},
                {"role": "user", "content": prompt}
            ]
        )
        diseases = response["choices"][0]["message"]["content"]
        # Ensure only valid diseases are kept
        return [d.strip() for d in diseases.split(",") if d.strip() in valid_diseases]
    except Exception as e:
        print("Error calling OpenAI:", e)
        return []

# Load preprocessed diet dataset
disease_diet_map = pd.read_csv(DIET_FILE_PATH)

def recommend_diet(diseases: List[str]) -> str:
    """
    Matches extracted diseases to recommended diets based on the preprocessed dataset.
    Returns a combined diet recommendation.
    """
    matched_diets = set()

    for disease in diseases:
        matching_rows = disease_diet_map[disease_diet_map["Disease"].str.contains(disease, case=False, na=False)]
        matched_diets.update(matching_rows["Diet"].tolist())

    return ", ".join(matched_diets) if matched_diets else "No specific diet recommendation available."

def parse_disease_and_recommend_diet(history: str) -> Dict:
    """
    Extracts diseases and recommends a diet based on a validated disease list.
    """
    diseases = parse_disease_history(history)
    recommended_diet = recommend_diet(diseases)

    return {
        "diseases": diseases,
        "recommended_diet": recommended_diet
    }
