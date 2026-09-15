from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from backend.app.schemas import HealthResponse
from backend.app.database import get_db

router = APIRouter(prefix="/health", tags=["health"])

@router.get("/")
async def health_check(db: AsyncSession = Depends(get_db)):
    """Zkontroluje, zda je backend a databáze v provozu."""
    await db.execute(text("SELECT 1"))
    return HealthResponse()
