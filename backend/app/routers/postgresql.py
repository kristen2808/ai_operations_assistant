from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.database import get_db
from backend.app.schemas import PostgreSQLConnectionsResponse
from backend.app.services.postgresql import get_connection_stats


router = APIRouter(
    prefix="/diagnostics/postgresql",
    tags=["PostgreSQL Diagnostics"],
)


@router.get("/connections", response_model=PostgreSQLConnectionsResponse)
async def get_connections(db: AsyncSession = Depends(get_db)):
    return await get_connection_stats(db)
