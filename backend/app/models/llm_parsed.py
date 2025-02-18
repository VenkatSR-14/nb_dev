from pydantic import BaseModel
from typing import List, Optional

class DiseaseHistoryRequest(BaseModel):
    history: str
    img_url: Optional[str] = None  # ✅ Allow optional image input

class ParsedDiseaseResponse(BaseModel):
    diseases: List[str]
    recommended_diet: str
