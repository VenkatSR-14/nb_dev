from fastapi import APIRouter, HTTPException
from models.llm_parsed import DiseaseHistoryRequest, ParsedDiseaseResponse
from services.llm_service import LLMService

router = APIRouter()

@router.post("/parse-disease-history", response_model=ParsedDiseaseResponse)
async def parse_disease(request: DiseaseHistoryRequest):
    """
    API endpoint to extract diseases and recommend a diet.
    Uses LLMService to call the business logic.
    Supports both text and optional image input.
    """
    result = LLMService.process_disease_history(request.history, request.img_url)  # ✅ Use request.img_url
    
    if not result["diseases"]:
        raise HTTPException(status_code=400, detail="No diseases detected")

    return result
