from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.routes.api import router as ai_router

app = FastAPI(title="Rentlora AI Service")

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(ai_router, prefix="/api/ai", tags=["AI"])

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "rentlora-ai-service"}
