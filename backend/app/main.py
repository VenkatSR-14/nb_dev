from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.v1 import api_router
from core.config import settings

app = FastAPI(
    title="NutriBuddy API",
    description="API for parsing disease history and recommending diets",
    version="1.0",
)

# Enable CORS (so frontend can access API)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change this to frontend domain for security
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register API Routes
app.include_router(api_router, prefix="/api/v1")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=settings.API_PORT)
