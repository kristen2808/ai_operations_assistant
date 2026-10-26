from datetime import datetime, timezone

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.database import get_db
from backend.app.models import DiagnosticRun
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


@router.post("/connections/run", response_model=PostgreSQLConnectionsResponse)
async def run_connections(db: AsyncSession = Depends(get_db)):
    started_at = datetime.now(timezone.utc)
    result = await get_connection_stats(db)
    finished_at = datetime.now(timezone.utc)

    diagnostic_run = DiagnosticRun(
        check_type="postgresql_connections",
        started_at=started_at,
        finished_at=finished_at,
        result=result,
    )
    try:
        db.add(diagnostic_run)
        await db.commit()
    except Exception:
        await db.rollback()
        raise

    return result
