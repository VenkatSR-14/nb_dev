from pydantic import BaseModel
from typing import List

class DiseaseHistoryRequest(BaseModel):
    history: str

class ParsedDiseaseResponse(BaseModel):
    diseases: List[str]
    recommended_diet: str