from fastapi import APIRouter
from app.api.v1.endpoints.users import router as users_router
from app.api.v1.endpoints.llm import router as llm_router
from app.api.v1.endpoints.auth import router as auth_router  # ✅ Import the correct auth router

api_router = APIRouter()

# ✅ Register routes
api_router.include_router(users_router, prefix="/users", tags=["Users"])
api_router.include_router(llm_router, prefix="/llm", tags=["LLM"])
api_router.include_router(auth_router, prefix="/auth", tags=["Authentication"])  # ✅ Corrected from llm_router to auth_router
