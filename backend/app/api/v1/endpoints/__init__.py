from fastapi import APIRouter
from app.api.v1.endpoints.users import router as users_router
from app.api.v1.endpoints.llm import router as llm_router
from app.api.v1.endpoints.recommender import router as recommender_router

api_router = APIRouter()

# ✅ Register all API routes in a single place
api_router.include_router(users_router, prefix="/users", tags=["Users"])
api_router.include_router(llm_router, prefix="/llm", tags=["LLM"])
api_router.include_router(recommender_router, prefix="/recommender", tags=["Recommender"])