from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.database import get_db
from backend.app.schemas import PostgreSQLConnectionsResponse
from backend.app.schemas import PostgreSQLLongRunningQueryResponse
from backend.app.services.postgresql import get_connection_stats
from backend.app.services.postgresql import get_long_running_queries


router = APIRouter(
    prefix="/diagnostics/postgresql",
    tags=["PostgreSQL Diagnostics"],
)


@router.get("/connections", response_model=PostgreSQLConnectionsResponse)
async def get_connections(db: AsyncSession = Depends(get_db)):
    return await get_connection_stats(db)


@router.get(
    "/long-running-queries", response_model=list[PostgreSQLLongRunningQueryResponse]
)
async def get_long_running_queries_endpoint(
    min_duration_seconds: int = Query(default=30, ge=1),
    db: AsyncSession = Depends(get_db),
):
    return await get_long_running_queries(
        db, min_duration_seconds=min_duration_seconds
    )
