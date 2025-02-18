# app/api/v1/__init__.py

from fastapi import APIRouter
from app.api.v1.endpoints.users import router as users_router  # ✅ Import user routes (or any other routes)

api_router = APIRouter()

# Include different route modules
api_router.include_router(users_router, prefix="/users", tags=["Users"])  # ✅ Register users routes
