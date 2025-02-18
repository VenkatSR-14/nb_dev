import openai
import pandas as pd
from typing import List, Dict, Optional
from app.core.config import settings

# ✅ Create OpenAI client (New OpenAI API Format)
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

import openai
import pandas as pd
from typing import List, Dict, Optional
from app.core.config import settings

# ✅ Set OpenAI API Key properly
openai.api_key = settings.OPENAI_API_KEY

def parse_disease_history(history: str, img_url: Optional[str] = None) -> List[str]:
    """
    Uses GPT-3.5-Turbo to extract diseases ONLY from the preprocessed user profile dataset.
    Supports both text and optional image input.
    """
    valid_diseases_str = ", ".join(valid_diseases)

    prompt = (
        f"Extract diseases from the following medical history:\n\n{history}\n\n"
        f"Return ONLY diseases in this list: {valid_diseases_str}.\n"
        f"Return diseases as a comma-separated format."
    )

    try:
        # ✅ Fix: Use `client.chat.completions.create()`
        messages = [
            {
                "role": "user",
                "content": [{"type": "text", "text": prompt}],
            }
        ]

        if img_url:
            messages[0]["content"].append(
                {
                    "type": "image_url",
                    "image_url": {"url": img_url},
                }
            )

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",  # ✅ Using GPT-3.5-Turbo
            messages=messages
        )

        diseases = response.choices[0].message.content.strip()
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

def parse_disease_and_recommend_diet(history: str, img_url: Optional[str] = None) -> Dict:
    """
    Extracts diseases and recommends a diet based on a validated disease list.
    Supports optional image input.
    """
    diseases = parse_disease_history(history, img_url)
    recommended_diet = recommend_diet(diseases)

    return {
        "diseases": diseases,
        "recommended_diet": recommended_diet
    }
