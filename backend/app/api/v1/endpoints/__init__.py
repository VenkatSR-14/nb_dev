from fastapi import APIRouter
from app.api.v1.endpoints.users import router as users_router
from app.api.v1.endpoints.llm import router as llm_router  # ✅ Import LLM routes

api_router = APIRouter()

# ✅ Register routes
api_router.include_router(users_router, prefix="/users", tags=["Users"])
api_router.include_router(llm_router, prefix="/llm", tags=["LLM"])  # ✅ Ensure this is included
