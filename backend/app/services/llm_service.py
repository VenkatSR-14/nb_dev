from core.llm_integration import parse_disease_and_recommend_diet
from typing import Dict

class LLMService:
    @staticmethod
    def process_disease_history(history: str) -> Dict:
        """
        Calls the LLM integration to extract diseases and recommend a diet.
        """
        return parse_disease_and_recommend_diet(history)
