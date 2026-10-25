from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession


async def get_connection_stats(db: AsyncSession) -> dict:
    result = await db.execute(
        text(
            """
            SELECT
                COUNT(*) AS total,
                COUNT(*) FILTER (WHERE state = 'active') AS active,
                COUNT(*) FILTER (WHERE state = 'idle') AS idle,
                COUNT(*) FILTER (
                    WHERE state = 'idle in transaction'
                ) AS idle_in_transaction
            FROM pg_stat_activity
            WHERE backend_type = 'client backend'
            """
        )
    )
    return dict(result.mappings().one())


async def get_long_running_queries(
    db: AsyncSession, min_duration_seconds: int = 30
) -> list[dict]:
    result = await db.execute(
        text(
            """
            SELECT
                pid,
                datname,
                usename,
                EXTRACT(EPOCH FROM clock_timestamp() - query_start)
                    AS duration_seconds,
                query
            FROM pg_stat_activity
            WHERE state = 'active'
                AND pid <> pg_backend_pid()
                AND EXTRACT(EPOCH FROM clock_timestamp() - query_start)
                    >= :min_duration_seconds
            """
        ),
        {"min_duration_seconds": min_duration_seconds},
    )
    return [dict(row) for row in result.mappings().all()]
