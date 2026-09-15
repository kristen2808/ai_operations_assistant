from backend.app.database import engine
from sqlalchemy import text

from backend.app.routers import api_router
from backend.app.schemas import HealthResponse
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.app.database import get_db

app = FastAPI(
    title="AI Operations Assistant API",
    description="Backend API pro AI Operations Assistant aplikaci",
    version="0.1.0",
)

# Nastavení CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # V production ztížit
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create tables on startup
@app.on_event("startup")
async def startup_db_event():
    async with engine.begin() as conn:
        await conn.execute(text("SELECT 1"))  # Test connection

# Mount API routes
app.include_router(api_router, prefix="/api/v1")

@app.get("/", response_model=dict)
async def root():
    return {
        "message": "AI Operations Assistant API",
        "version": "0.1.0",
        "docs": "/docs",
    }