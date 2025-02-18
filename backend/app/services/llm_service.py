from app.core.llm_integration import parse_disease_and_recommend_diet
from typing import Dict, Optional

class LLMService:
    @staticmethod
    def process_disease_history(history: str, img_url: Optional[str] = None) -> Dict:
        """
        Calls the LLM integration to extract diseases and recommend a diet.
        Supports optional image input.
        """
        return parse_disease_and_recommend_diet(history, img_url)  # ✅ Pass `img_url`
