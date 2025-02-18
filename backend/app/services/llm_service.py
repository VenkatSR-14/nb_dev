from app.core.llm_integration import parse_disease_and_recommend_diet
from typing import Optional

class LLMService:
    @staticmethod
    def process_disease_history(history: str, img_url: Optional[str] = None):
        if not history.strip():
            return {"diseases": [], "recommended_diet": "No history provided."}  # ✅ Handle empty input

        result = parse_disease_and_recommend_diet(history, img_url)

        if not result.get("diseases"):
            return {"diseases": [], "recommended_diet": "No diseases detected."}  # ✅ Prevent OpenAI failures

        return result
